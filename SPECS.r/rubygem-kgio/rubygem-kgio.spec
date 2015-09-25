%global gem_name kgio

%if 0%{?fedora} >= 19
  %global rubyabi 2.0.0
%endif

Summary:       Kinder, gentler I/O for Ruby
Name:          rubygem-%{gem_name}
Version:       2.9.3
Release:       3%{?dist}
Group:         Development/Tools
License:       LGPLv2 or LGPLv3
# LICENSE file defines the licencing aspects of kgiox.
# No license info in source files. 
URL:           http://bogomips.org/kgio
Source0:       http://rubygems.org/downloads/%{gem_name}-%{version}.gem

%if 0%{?fedora} >= 19 && 0%{?fedora} < 21
Requires:       ruby(release)
%endif

BuildRequires: ruby-devel
BuildRequires: ruby-irb
BuildRequires: rubygems-devel
BuildRequires: rubygem(test-unit)
%if 0%{?fedora} < 21
Provides:      rubygem(%{gem_name}) = %{version}
%endif
ExcludeArch:   ppc ppc64

%description
kgio provides non-blocking I/O methods for Ruby without raising
exceptions on EAGAIN and EINPROGRESS.  It is intended for use with the
Unicorn and Rainbows! Rack servers, but may be used by other
applications (that run on Unix-like platforms).

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Remove the binary extension sources and build leftovers.
rm -f %{buildroot}%{gem_instdir}/.document
rm -f %{buildroot}%{gem_instdir}/.gitignore
rm -f %{buildroot}%{gem_instdir}/.manifest
rm -f %{buildroot}%{gem_instdir}/.olddoc.yml
rm -f %{buildroot}%{gem_instdir}/pkg.mk
rm -f %{buildroot}%{gem_instdir}/setup.rb
rm -f %{buildroot}/%{gem_instdir}/kgio.gemspec
rm -f %{buildroot}/%{gem_instdir}/GNUmakefile
rm -f %{buildroot}/%{gem_instdir}/GIT-VERSION-FILE
rm -f %{buildroot}/%{gem_instdir}/GIT-VERSION-GEN
rm -rf %{buildroot}%{gem_instdir}/archive
rm -rf %{buildroot}%{gem_instdir}/ext

# If there are C extensions, mv them to the extdir.
# You must replace REQUIRE_PATHS according to your gem specifics.
%if 0%{?fedora} >= 19 && 0%{?fedora} < 21
install -d m0755 %{buildroot}%{gem_extdir_mri}/lib
mv %{buildroot}%{gem_instdir}/lib/kgio_ext.so %{buildroot}%{gem_extdir_mri}/lib/
%endif


%if 0%{?fedora} >= 21
install -d m0755 %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,kgio_ext.so} %{buildroot}%{gem_extdir_mri}/
%endif

%check
pushd .%{gem_instdir}
ruby -Ilib:$(dirs +1)%{gem_extdir_mri} -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files doc
%doc %{gem_dir}/doc/%{gem_name}-%{version}
%doc %{gem_instdir}/TODO
%doc %{gem_instdir}/LATEST
%doc %{gem_instdir}/ISSUES
%doc %{gem_instdir}/HACKING
%doc %{gem_instdir}/test

%files
%if 0%{?fedora} >= 19
%{gem_extdir_mri}
%endif

%dir %{gem_instdir}/lib
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/README
%doc %{gem_instdir}/NEWS
%exclude %{gem_cache}
%{gem_spec} 
%{gem_instdir}/lib/kgio.rb

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.9.3-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 2.9.3-1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2
- Update to kgio 2.9.3.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 25 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 2.8.0-5
- Fixes for Ruby 2.1 packaging guidelines (#1096996, #1107152)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 23 2013 Guillermo Gómez <guillermo.gomez@gmail.com> - 2.8.0-2
- Fixes for Ruby 2.0.0 packaging guidelines

* Sun Feb 10 2013 Guillermo Gómez <guillermo.gomez@gmail.com> - 2.8.0-1
- Update version 2.8.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Guillermo Gómez <guillermo.gomez@gmail.com> - 2.7.3-1
- Update version 2.7.3

* Sun Feb 12 2012 Guillermo Gómez <guillermo.gomez@gmail.com> - 2.7.0-5
- Proper use of new macros for Ruby 1.9 packaging
- irb added as build require

* Sat Jan 07 2012 Guillermo Gómez <guillermo.gomez@gmail.com> - 2.7.0-4
- Requires fixed for Ruby 1.9

* Sun Jan 01 2012 Guillermo Gómez <guillermo.gomez@gmail.com> - 2.7.0-3
- Path to kgio_ext.so at spec file check section fixed
- Moved patching test file to install section
- Unused macro removed from spec file

* Sat Dec 31 2011 Guillermo Gómez <guillermo.gomez@gmail.com> - 2.7.0-2
- For now rdoc-generated files arch-dependent
- defattr at the beginning of files remove
- README, NEWS, ChangeLog location fixed
- Test suite enabled during build time
- kgio_ext.so placed under ruby_sitearch dir

* Fri Dec 30 2011 Guillermo <guillermo.gomez@gmail.com> - 2.7.0-1
- Initial package
