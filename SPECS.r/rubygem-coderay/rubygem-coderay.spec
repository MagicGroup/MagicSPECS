%global gem_name coderay

Summary: Fast syntax highlighter engine for many programming languages
Name: rubygem-%{gem_name}
Version: 1.1.0
Release: 7%{?dist}
Group: Development/Languages
License: LGPLv2+
URL: http://coderay.rubychan.de
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(release)
Requires: ruby(rubygems)
#BuildRequires: rubygem(term-ansicolor)
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Coderay is a Ruby library for syntax highlighting. CodeRay is build to be easy
to use and intuitive, but at the same time fully featured, complete, fast and
efficient. 


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

rm -rf %{buildroot}/%{gem_libdir}/term

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x
find %{buildroot}/%{gem_instdir}/bin -type f | xargs sed -i 's/\r//' $FILES

%files 
%{_bindir}/coderay
%dir %{gem_instdir}/
%dir %{gem_libdir}
%dir %{gem_instdir}/test
%{gem_instdir}/test/*
%{gem_instdir}/bin
%{gem_libdir}/[cC]*
%doc %{gem_docdir}
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/README_INDEX.rdoc
%exclude %{gem_cache}
%{gem_spec}


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.1.0-7
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.0-6
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 15 2014 Jan Klepek <jan.klepek at, gmail.com> -1.1.0-3
- dropped dependency on term-ansicolor completely

* Mon Mar 3 2014 Jan Klepek <jan.klepek at, gmail.com> - 1.1.0-2
- term-ansicolor no longer run-time dependency, only build dependency

* Thu Feb 27 2014 Jan Klepek <jan.klepek at, gmail.com> - 1.1.0-1
- update to new version

* Mon Aug 19 2013 Jan Klepek <jan.klepek at, gmail.com> - 1.0.7-1
- update to new version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 05 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.6-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 08 2012 Jan Klepek <jan.klepek at, gmail.com> - 1.0.6-1
- Update to new version

* Mon Feb 06 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.4-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Jan Klepek <jan.klepek at, gmail.com> - 1.0.4-1
- new version

* Sat Oct 15 2011 Jan Klepek <jan.klepek at, gmail.com> - 1.0.0-1
- new version

* Sat Jul 23 2011 Jan Klepek <jan.klepek at, gmail.com> - 0.9.8-1
- new version

* Thu Mar 10 2011 Jan Klepek <jan.klepek at, gmail.com> - 0.9.7-1
- updated to 0.9.7

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.312-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.312-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 03 2009 Jan Klepek <jan.klepekat, gmail.com> - 0.8.312-3
- correct directory ownership, fixed license

* Wed Jun 24 2009 Jan Klepek <jan.klepekat, gmail.com> - 0.8.312-2
- consistent macro usage, rewritten description, removed term-ansicolor during install

* Sun Jun 14 2009 Jan Klepek <jan.klepekat, gmail.com> - 0.8.312-1
- Initial package
