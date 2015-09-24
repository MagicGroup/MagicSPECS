# Generated from net-ssh-2.2.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name net-ssh

Summary: Net::SSH: a pure-Ruby implementation of the SSH2 client protocol
Name: rubygem-%{gem_name}
Version: 2.9.1
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/net-ssh/net-ssh
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(mocha)
BuildRequires: ruby 
BuildArch: noarch

%description
Net::SSH: a pure-Ruby implementation of the SSH2 client protocol.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

            
%check
pushd .%{gem_instdir}
# Some test cases fails.
# https://github.com/net-ssh/net-ssh/issues/167
ruby -Ilib -Itest test/test_all.rb | \
  grep "2041 tests, 6175 assertions, 0 failures, 88 errors, 0 pendings, 0 omissions, 0 notifications"
popd


%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/support
%exclude %{gem_instdir}/setup.rb
%exclude %{gem_instdir}/.*
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/THANKS.txt
%doc %{gem_instdir}/CHANGES.txt
%{gem_instdir}/gem-public_cert.pem
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_docdir}
%{gem_instdir}/Manifest
%{gem_instdir}/Rakefile
%{gem_instdir}/Rudyfile
%{gem_instdir}/test
# Required to run tests
%{gem_instdir}/net-ssh.gemspec

%changelog
* Thu Jul 03 2014 Vít Ondruch <vondruch@redhat.com> - 2.9.1-1
- Update to net-ssh 2.9.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 2.6.6-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to net-ssh 2.6.6.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.2.1-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 04 2011 Shreyank Gupta <sgupta@redhat.com> - 2.2.1-1
- Updated to version 2.2.1-1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 24 2010 Adam Tkac <atkac redhat com> - 2.0.23-5
- rebuild to ensure F14 has higher NVR than F13

* Fri Jun 11 2010 Shreyank Gupta <sgupta@redhat.com> - 2.0.23-4
- Bring back the BR: rubygem(rake) and rake test

* Thu Jun 10 2010 Shreyank Gupta <sgupta@redhat.com> - 2.0.23-3
- test command from test/README.txt
- Remove gem "test-unit" line
- Removed Requires rubygem(rake)
- BuildRequires/Requires: rubygem(mocha) for tests

* Thu Jun 10 2010 Shreyank Gupta <sgupta@redhat.com> - 2.0.23-2
- Using %%exclude for setup.rb
- Keeping net-ssh.gemspec for tests
- Moved file-not-utf8 correction to before %%check section

* Wed Jun 09 2010 Shreyank Gupta <sgupta@redhat.com> - 2.0.23-1
- Initial package
