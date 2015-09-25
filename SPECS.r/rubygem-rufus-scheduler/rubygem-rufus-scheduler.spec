# Generated from rufus-scheduler-1.0.11.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rufus-scheduler

Summary:       Scheduler for Ruby (at, cron and every jobs)
Name:          rubygem-%{gem_name}
Version:       2.0.4
Release:       10%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://openwferu.rubyforge.org/scheduler.html
Source0:       http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      ruby(release)
Requires: ruby(rubygems)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildArch:     noarch
Provides:      rubygem(%{gem_name}) = %{version}

%description
job scheduler for Ruby (at, cron, in and every jobs)

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}
chmod +x %{buildroot}%{gem_instdir}/test/*rb

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{gem_libdir}
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.txt
%doc %{gem_instdir}/CREDITS.txt
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/TODO.txt
%{gem_instdir}/misc
%{gem_instdir}/Rakefile
%{gem_instdir}/spec
%{gem_instdir}/test
%{gem_instdir}/%{gem_name}.gemspec
%{gem_cache}
%{gem_spec}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.4-10
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.4-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 2.0.4-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 16 2010 Darryl L. Pierce <dpierce@redhat.com> - 2.0.4-1
- Made tests executable if they have a hashbang.
- Release 2.0.4 of Rufus Scheduler.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 10 2009 Darryl Pierce <dpierce@redhat.com> - 2.0.1-2
- Second release due to errors in tagging.

* Sun May 10 2009 Darryl Pierce <dpierce@redhat.com> - 2.0.1-1
- Release 2.0.1 of Rufus Scheduler.

* Fri May  1 2009 Darryl Pierce <dpierce@redhat.com> - 1.0.14-1
- Release 1.0.14 of rufus-scheduler.

* Thu Apr 30 2009 Darryl Pierce <dpierce@redhat.com> - 1.0.13-3
- First official build for Fedora.

* Wed Apr 29 2009 Darryl Pierce <dpierce@redhat.com> - 1.0.13-2
- Added reference to license file.
- Removed ruby_sitelib macro.
- Added ruby(abi) Requires.

* Mon Feb 02 2009 Darryl Pierce <dpierce@redhat.com> - 1.0.13-1
- Release 1.0.13 of rufus-scheduler.

* Thu Dec 18 2008 Darryl Pierce <dpierce@redhat.com> - 1.0.12-1
- Release 1.0.12 of the gem.

* Mon Nov 24 2008 Darryl Pierce <dpierce@redhat.com> - 1.0.11-1
- Initial package
