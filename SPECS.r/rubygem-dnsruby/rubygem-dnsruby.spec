# Generated from dnsruby-1.52.gem by gem2rpm -*- rpm-spec -*-
%global gem_name dnsruby


Summary: Ruby DNS(SEC) implementation
Name: rubygem-%{gem_name}
Version: 1.53
Release: 9%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://rubyforge.org/projects/dnsruby/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: ruby 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Dnsruby is a pure Ruby DNS client library. It provides a complete DNS
client implementation, including DNSSEC. It can also load (BIND) zone
files. Dnsruby has been used in OpenDNSSEC and ISC's DLV service.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
# ri installs bad filenames with macros in it, see rhbz#711893
# Reported to upstream
%gem_install -n %{SOURCE0}

%build

# Requires network traffic, also contains errors and seems to never return
#% check
#pushd .% {gem_instdir}
#RUBYOPT=rubygems testrb test/*.rb
#popd

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
# fix some DOS formated file
sed -i 's/\r//' %{buildroot}%{gem_instdir}/README
sed -i 's/\r//' %{buildroot}%{gem_instdir}/DNSSEC

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/test
%{gem_instdir}/demo
%{gem_instdir}/Rakefile
%{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/README

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/DNSSEC
%doc %{gem_instdir}/EXAMPLES
%doc %{gem_instdir}/README
%doc %{gem_instdir}/EVENTMACHINE


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.53-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.53-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.53-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.53-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.53-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.53-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.53-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 18 2011 Paul Wouters <paul@xelerance.com> - 1.53-1
- Updated to 1.53

* Fri Oct 14 2011 Paul Wouters <paul@xelerance.com> - 1.52-3
- Initial package
- Re-enabled ri install

* Tue Oct 04 2011 Paul Wouters <paul@xelerance.com> - 1.52-2
- Initial package for review
