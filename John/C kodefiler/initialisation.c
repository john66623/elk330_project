double pmeas;

pmeas = 0.;
SOC = SOCini;
SOCnext = SOC;
limitP = 0;

!Get the step size of the QDS
timeDif = GetStepSizeSeconds();

! measured power operation area
chargeP = 0.;
if ({PFullStore <= PStartStore}.or.{-PStartFeed <= -PFullFeed}) {
  chargeP = 0;  ! Error
  Warn('PFullStore must be > than PStartStore and PFullFeed > than PStartFeed');
}
else if (pmeas < PStartFeed) {
  chargeP = 3;
}
else if (pmeas > PStartStore) {
  chargeP = 1;
}
else {
  chargeP = 2;
}

! energy operation area
iniSOCoob = 0; ! Inside bounds
if (SOCmin >= SOCmax) {
  chargeE = 0;  ! Error
  Warn('SOCmin must be < than SOCmax.');  
}
else if (SOC > SOCmax) {
  chargeE = 3;
  iniSOCoob = 1;
}
else if (SOC = SOCmax) {
  chargeE = 3;
}
else if (SOC = SOCmin) {
  chargeE = 1;
}
else if (SOC < SOCmin) {
  chargeE = 1;
  iniSOCoob = 1;
}
else {
  chargeE = 2;
}
