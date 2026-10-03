import unittest
import numpy as np
from tools.audit_amr_mean_transfer import transfer_diagnostics


class TransferDiagnosticsTests(unittest.TestCase):
    def test_refined_children_copy_parent_and_preserve_integral(self):
        n=2; h=np.pi
        c=np.stack(np.meshgrid(*[(np.arange(n)+.5)*h]*3,indexing='ij'),axis=-1).reshape(-1,3)
        make=lambda c,v,u: dict(cx=c[:,0],cy=c[:,1],cz=c[:,2],V=v,Ux=u[:,0],Uy=u[:,1],Uz=u[:,2],p=u[:,0]/2)
        u=np.arange(24,dtype=float).reshape(8,3)+1
        pre=make(c,np.full(8,h**3),u)
        offsets=np.stack(np.meshgrid(*[np.array([-.25,.25])*h]*3,indexing='ij'),axis=-1).reshape(-1,3)
        cc=np.concatenate((c[:1]+offsets,c[1:])); cv=np.concatenate((np.full(8,h**3/8),np.full(7,h**3)))
        cu=np.concatenate((np.repeat(u[:1],8,axis=0),u[1:]))
        mapped=make(cc,cv,cu)
        result=transfer_diagnostics(pre,mapped,n)
        self.assertTrue(result['exact_captured_parent_value_copy'])
        self.assertLess(result['velocity_integral_difference_relative_to_parent_l1'],1e-15)
        self.assertLess(abs(result['velocity_p0_total_squared_difference']),1e-8)
        self.assertLess(abs(result['velocity_mean_error_floor_exchange_identity_residual']),1e-8)
        mapped['Ux'][0]+=.25
        changed=transfer_diagnostics(pre,mapped,n)
        self.assertFalse(changed['exact_captured_parent_value_copy'])
        self.assertEqual(changed['velocity_parent_injection_max_absolute_difference'],.25)
        self.assertGreater(changed['velocity_integral_difference_relative_to_parent_l1'],0)

    def test_duplicate_parent_geometry_and_nan_do_not_form_valid_diagnostic(self):
        n=2;h=np.pi;c=np.stack(np.meshgrid(*[(np.arange(n)+.5)*h]*3,indexing='ij'),axis=-1).reshape(-1,3)
        d=dict(cx=c[:,0].copy(),cy=c[:,1].copy(),cz=c[:,2].copy(),V=np.full(8,h**3),Ux=np.ones(8),Uy=np.ones(8),Uz=np.ones(8),p=np.ones(8))
        for key in ('cx','cy','cz'):d[key][1]=d[key][0]
        with self.assertRaisesRegex(ValueError,'duplicated'):transfer_diagnostics(d,d,n)
        for j,key in enumerate(('cx','cy','cz')):d[key]=c[:,j].copy()
        d['Ux'][0]=np.nan
        with self.assertRaisesRegex(ValueError,'nonfinite'):transfer_diagnostics(d,d,n)
