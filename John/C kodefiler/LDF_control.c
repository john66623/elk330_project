Pmeas = Pload*orientation; ! negative=load

! measured power operation area

if (chargeP > 0) {  ! Not initial error
  if ({chargeRequired = 1}.and.{SOC < SOCmax}) {
    chargeP = 1; ! Charging towards kl. 7
  }
  else {
    ! Existing power-based control
    if (Pmeas < -PStartFeed) {
      chargeP = 3;
    }
    else if (Pmeas > PStartStore) {
      chargeP = 1;
    }
    else {
      chargeP = 2;
    }
  }
}

! Check if car is home
if ({hour < 16}.and.{hour > 07}) {
  chargeP = 2;
}


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
