%global gem_name kwalify

Summary: A parser, schema validator, and data-binding tool for YAML and JSON
Name: rubygem-%{gem_name}
Version: 0.7.2
Release: 10%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.kuwata-lab.com/kwalify
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires: ruby(release)
Requires: ruby(rubygems)
Requires: ruby
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Kwalify is a parser, schema validator, and data binding tool for YAML and
JSON.

%package doc
Summary: Documentation for %{name}
Group: Documentation
License: MIT and LGPLv2
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep

%build

%install
mkdir -p %{buildroot}%{gem_dir}
gem install --bindir %{buildroot}/%{_bindir} --local --install-dir %{buildroot}%{gem_dir} \
            --force --rdoc %{SOURCE0}

%files
%dir %{gem_instdir}
%{_bindir}/kwalify
%{gem_instdir}/bin
%{gem_instdir}/contrib
%{gem_libdir}
%doc %{gem_instdir}/CHANGES.txt
%doc %{gem_instdir}/README.txt
%doc %{gem_instdir}/MIT-LICENSE
%{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/doc
%{gem_instdir}/doc-api
%{gem_instdir}/examples
%{gem_instdir}/test
%{gem_instdir}/setup.rb
%{gem_docdir}

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 17 2013 Marek Goldmann <mgoldman@redhat.com> - 0.7.2-8
- New guidelines

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.7.2-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Apr 08 2011 Marek Goldmann <mgoldman@redhat.com> - 0.7.2-3
- Cleaned spec file, again.

* Thu Apr 07 2011 Marek Goldmann <mgoldman@redhat.com> - 0.7.2-2
- Cleaned spec file

* Thu Mar 31 2011 Marek Goldmann <mgoldman@redhat.com> - 0.7.2-1
- Initial package
