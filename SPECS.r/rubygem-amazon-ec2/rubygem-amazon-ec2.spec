%global gem_name amazon-ec2

Summary: Amazon EC2 Ruby Gem
Name: rubygem-%{gem_name}
Version: 0.9.15
Release: 12%{?dist}
Group: Development/Languages
License: GPLv2 or Ruby
URL: http://github.com/grempe/amazon-ec2
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(release)
Requires: rubygem(xml-simple)
BuildRequires: rubygems-devel
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(test-spec)
BuildRequires: rubygem(rake)
BuildRequires: rubygem(xml-simple)
BuildRequires: rubygem(mocha) >= 0.9.8
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A Ruby library for accessing the Amazon Web Services EC2, ELB, RDS,
Cloudwatch, and Autoscaling APIs.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}/%{_bindir}
mv .%{_bindir}/ec2sh %{buildroot}/%{_bindir}
mv .%{gem_dir}/* %{buildroot}/%{gem_dir}
rm -f %{buildroot}%{gem_instdir}/.yardopts
rm -f %{buildroot}%{gem_instdir}/.gitignore
sed -i 's/\r//' %{buildroot}%{gem_instdir}/wsdl/2008-02-01.ec2.wsdl

%check
pushd %{buildroot}/%{gem_instdir}
ruby -Ilib -e "Dir.glob('./test/**/test_*').each {|t| require t}"
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}
%{_bindir}/ec2sh
%{gem_instdir}/bin
%{gem_libdir}
%doc %{gem_instdir}/ChangeLog
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/VERSION
%doc %{gem_instdir}/README.rdoc

%{gem_cache}
%{gem_spec}

%files doc
%defattr(-, root, root, -)
%{gem_instdir}/Rakefile
%{gem_instdir}/test
%{gem_instdir}/deps.rip
%{gem_instdir}/wsdl
%{gem_instdir}/perftools
%{gem_instdir}/README_dev.rdoc
%{gem_instdir}/%{gem_name}.gemspec
%{gem_docdir}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.9.15-12
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 21 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.15-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.9.15-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.15-3
- Moved some documentation to main package
- Set proper attr on documentation package

* Wed Oct 06 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.15-2
- Removed unused macros
- Fixed license and version dependencies
- Moved documentation files into -doc subpackage

* Fri Oct 01 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.15-1
- Initial package
