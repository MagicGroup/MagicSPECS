# Some R modules are not smart enough to ask R for the value of RHOME
# and instead depend on the R_HOME environment variable.
# Set R_HOME only if it is not already set.
if ( ${?R_HOME} == 0 ) then
  set RHOME = `R RHOME`
  setenv R_HOME $RHOME
endif
