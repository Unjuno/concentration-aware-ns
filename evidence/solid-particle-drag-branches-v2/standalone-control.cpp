#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
// Source-transcribed, one-dimensional positive carrier velocity; nu=d=rho/rhop=1,
// dt=1, initial particle velocity and gravity=0. Not an OpenFOAM cloud execution.
double update(double u) {
    double speed=std::sqrt(u*u);
    double correction=1;
    if (speed>0.01) correction+=0.15*std::pow(speed,0.687);
    double drag=18*correction;
    return drag*u/(1+drag);
}
int main() {
    double low=0.01,high=std::nextafter(low,std::numeric_limits<double>::infinity());
    double a=update(low),b=update(high);
    std::cout<<std::setprecision(17)<<"{\"carrier_low\":"<<low<<",\"carrier_high\":"<<high
      <<",\"carrier_difference\":"<<high-low<<",\"update_low\":"<<a<<",\"update_high\":"<<b
      <<",\"update_difference\":"<<b-a<<",\"finite_difference_gain\":"<<(b-a)/(high-low)<<"}\n";
}
