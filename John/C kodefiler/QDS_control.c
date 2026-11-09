! energy operation area
if (chargeE > 0) {  ! Not initial error
  if (SOC >= SOCmax) {
    chargeE = 3;
    if ({iniSOCoob = 0}.and.{SOC > SOCmax}) {
      SOC = SOCmax;
    }
  }
  else if (SOC <= SOCmin) {
    chargeE = 1;
    if ({iniSOCoob = 0}.and.{SOC < SOCmin}) {
      SOC = SOCmin;
    }
  }
  else {
    chargeE = 2;
    iniSOCoob = 0; ! Inside limits now
  }
}

! Check charging status in next time step
SOCnext = SOC + (-Pset * 100.) / (Eini * 3600.)*timeDif;
if (SOCnext >= SOCmax){
  limitP = 1; ! Battery is fully charged
}
else if (SOCnext <= SOCmin){
  limitP = -1; ! Battery is fully dischared
}
else{
  limitP = 0;
}

