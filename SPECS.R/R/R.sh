# Some R modules are not smart enough to ask R for the value of RHOME
# and instead depend on the R_HOME environment variable.
# Set R_HOME only if it is not already set.
test "a$R_HOME" = "a" && export R_HOME="`R RHOME`"
