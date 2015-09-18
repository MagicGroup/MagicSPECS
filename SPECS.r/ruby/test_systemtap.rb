require 'rbconfig'

if RbConfig::CONFIG.select {|k, v| v =~ /dtrace/}.size == 1
  exit true
else
  puts 'ERROR: SystemTap (dtrace) support was not detected.'

  exit false
end
