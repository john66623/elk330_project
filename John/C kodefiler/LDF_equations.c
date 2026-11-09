double Pgen,
       Qgen,
       simTime,
       redFac;

!!!!!!!!!!!!!! Kode for å hente døgntidspunkt, hour kommer ut som 0-24 basert på tid i døgnet
string timeStr;
int timeInt;

! Get current simulation time
simTime = GetSimulationTime();

! Convert to local date and time
timeStr = FormatDateLT('%Y-%m-%d %H:%M:%S', simTime);
simTime = ParseDateUTC('%Y-%m-%d %H:%M:%S', timeStr);

! Extract hour of day
simTime = simTime / (60. * 60. * 24.);
timeInt = floor(simTime);
hour = (simTime - timeInt) * 24.;
tid_ut_test = hour;
!!!!!!!!!!!!!!!!!!!!



timeDif = GetStepSizeSeconds();
redFac = 1.0;
Pmeas = Pload*orientation; ! negative=load

! if Discharge, between limits
if ({chargeP = 3}.and.{chargeE >= 2}.and.{chargeE > 0}) {
  
  if (limitP = -1){ ! restrict discharging power
    Pgen = ((SOC-SOCmin)*Eini*3600)/(timeDif*100);
  }
  
  else{
    Pgen = Ptowardsgrid - (Pmeas+Pline_PV);  ! discharge = GEN, feeding
    if (Pgen < 0){
      Pgen = 0.;
    }
    
  }
  
  Qgen = Qfeed;  ! discharge = GEN, feeding
}

! if Charge, between limits
else if ({chargeP = 1}.and.{chargeE <= 2}.and.{chargeE > 0}) {
  
  if (limitP = 1){ ! restrict charging power
    Pgen = ((SOC-SOCmax)*Eini*3600)/(timeDif*100);
  }
  
  else{
    Pgen = -Pstore;  ! charge = LOAD, storing
  }
  
  Qgen = -Qstore;  ! charge = LOAD, storing
}


! else (aka. fault or idle)
else {
  Pgen = 0.;
  Qgen = 0.;
}

!!! Beregning av gjenstående ladetid
tCharge = Eini * (SOCmax + 8. - SOC) / (100. * Pstore);

! Beregning av tid til klokka 7
if (hour < 7.) {
  tRemaining = 7. - hour;
}
else {
  tRemaining = 24. - hour + 7.;
}

! Bestemmelse om lading bør begynne
if (tCharge >= tRemaining) {
  chargeRequired = 1;
}
else {
  chargeRequired = 0;
}

! Calculating power for SOC reduction during the day
 Pdrive = Eini * SOCdrive / (100. * 9.);


SetEquation(0, Pset - Pgen);
SetEquation(1, Qset - Qgen);
