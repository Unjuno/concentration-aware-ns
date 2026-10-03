"""Enclose a real-arithmetic ball inside exactly one captured candidate tet."""
from flint import arb,arb_mat
from tools.amr_point_gradient_bound import exact_float
from tools.amr_arb_mean_certificate import endpoints


def barycentric_neighborhood(vertices,centre,radius):
    """Use affine weight Lipschitz constants to bound every point in the ball."""
    p=[[exact_float(v) for v in row] for row in vertices]
    if len(p)!=4 or any(len(row)!=3 for row in p) or len(centre)!=3 or not radius>0:
        raise ValueError('nondegenerate 3D tet and positive radius required')
    a=arb_mat([[p[i][j]-p[0][j] for i in (1,2,3)] for j in range(3)])
    determinant=a.det()
    if determinant.contains(0):raise ValueError('degenerate or unenclosed tetrahedron')
    inverse=a.inv();tail=inverse*arb_mat([[centre[j]-p[0][j]] for j in range(3)])
    weights=[1-sum((tail[i,0] for i in range(3)),arb(0))]+[tail[i,0] for i in range(3)]
    gradients=[[-sum((inverse[i,j] for i in range(3)),arb(0)) for j in range(3)]]+[[inverse[i,j] for j in range(3)] for i in range(3)]
    norms=[sum((x*x for x in row),arb(0)).sqrt() for row in gradients]
    lower=[(weights[i]-radius*norms[i]).lower() for i in range(4)]
    upper=[(weights[i]+radius*norms[i]).upper() for i in range(4)]
    return {'determinant':endpoints(determinant),'centre_weights':[endpoints(x) for x in weights],
            'weight_gradient_norm_upper':[endpoints(x.upper()) for x in norms],
            'ball_weight_lower':[endpoints(x) for x in lower],'ball_weight_upper':[endpoints(x) for x in upper],
            'strictly_inside_entire_ball':all(x>0 for x in lower),
            'strictly_outside_entire_ball':any(x<0 for x in upper)}


def unique_neighborhood(vertices,target,centre,radius):
    if not 0<=target<len(vertices):raise ValueError('target candidate missing')
    rows=[barycentric_neighborhood(p,centre,radius) for p in vertices]
    ok=rows[target]['strictly_inside_entire_ball'] and all(r['strictly_outside_entire_ball'] for i,r in enumerate(rows) if i!=target)
    return {'status':'UNIQUE_IDEALIZED_PIECE_ON_ENCLOSED_BALL' if ok else 'LOCAL_UNIQUENESS_NOT_CERTIFIED',
            'radius':endpoints(radius),'centre':[endpoints(x) for x in centre],'target_candidate':target,'candidates':rows}
