if ({hour < 16}.and.{hour > 07}) {
  SOC. = -Pdrive * 100. / (Eini * 3600.); ! SOC reduction during working hours (driving)
}

else {
  SOC. = -Pset * 100. / (Eini * 3600.);  ! slope of charge/discharge in %
}
