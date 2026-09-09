// Original benchmark control. u=(1+t*t,0,0), p=0, f=(2*t,0,0).
// Every spatial derivative vanishes on the periodic cube.
namespace {
void localized(const su2double*, su2double t, su2double, su2double* u, su2double* f) {
  u[0]=1+t*t;u[1]=0;u[2]=0;
  f[0]=2*t;f[1]=0;f[2]=0;
}
}
