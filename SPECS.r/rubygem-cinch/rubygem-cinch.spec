# Generated from cinch-2.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name cinch

Summary:       An IRC Bot Building Framework
Name:          rubygem-%{gem_name}
Version:       2.2.4
Release:       3%{?dist}
License:       MIT

URL:           http://cinchrb.org
Source0:       http://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildArch:     noarch

BuildRequires: ruby >= 1.9.1
BuildRequires: ruby(release)
BuildRequires: rubygems-devel

%if 0%{?fc20} || 0%{?el7}
Requires:      ruby(release)
Requires:      ruby(rubygems)

Provides:      rubygem(%{gem_name}) = %{version}
%endif


%description
A simple, friendly DSL for creating IRC bots.


%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch


%description doc
%{summary}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# clean up files that were included in them gem
rm -f \
   cinch-2.2.1/usr/share/gems/gems/cinch-2.2.1/lib/cinch/#channel.rb# \
   cinch-2.2.1/usr/share/gems/doc/cinch-2.2.1/rdoc/lib/cinch/#channel_rb#.html \
   cinch-2.2.1/usr/share/gems/doc/cinch-2.2.1/ri/lib/cinch/page-#channel_rb#.ri \
   cinch-2.2.1/lib/cinch/#channel.rb#


%build
gem build %{gem_name}.gemspec
%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# cleanup files that should not be installed
rm %{buildroot}%{gem_instdir}/.yardopts \
   %{buildroot}%{gem_instdir}/lib/cinch/#channel.rb#


%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/examples
%doc %{gem_instdir}/docs
%doc %{gem_instdir}/README.md

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.2.4-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 16 2015 Darryl L. Pierce <dpierce@redhat.com> - 2.2.4-1
- Rebased on Cinch 2.2.4.

* Tue Jan 13 2015 Darryl L. Pierce <dpierce@redhat.com> - 2.2.3-1
- Rebased on Cinch 2.2.3.
- Fixed the conditionals for the Requires to be easier to read.

* Tue Jan  6 2015 Darryl L. Pierce <dpierce@redhat.com> - 2.2.2-1
- Rebased on Cinch 2.2.2.
- Added condition to the Provides to be only on EPEL and F20

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar  5 2014 Darryl L. Pierce <dpierce@redhat.com> - 2.1.0-1
- Rebased on Cinch 2.1.0.
- Updated project URL.

* Fri Jan 31 2014 Darryl L. Pierce <dpierce@redhat.com. - 2.0.12-1
- Rebased on Cinch 2.0.12.

* Thu Dec 12 2013 Darryl L. Pierce <dpierce@redhat.com> - 2.0.11-1
- Rebased on Cinch 2.0.11.

* Wed Nov  6 2013 Darryl L. Pierce <dpierce@redhat.com> - 2.0.10-1
- Rebased on Cinch 2.0.10.

* Tue Sep  3 2013 Darryl L. Pierce <dpierce@redhat.com> - 2.0.9-1
- Rebased on Cinch 2.0.9.

* Mon Jul 29 2013 Darryl L. Pierce <dpierce@redhat.com> - 2.0.7-1
- Rebased on Cinch 2.0.7.

* Mon Jul 29 2013 Darryl L. Pierce <dpierce@redhat.com> - 2.0.6-1
- Rebased on Cinch 2.0.6.

* Fri Jun 21 2013 Darryl L. Pierce <dpierce@redhat.com> - 2.0.5-1
- Rebased on Cinch 2.0.5.

* Mon Mar 11 2013 Darryl L. Pierce <dpierce@redhat.com> - 2.0.4-1.1
- Updated the specfile for the current Ruby packaging guidelines.

* Wed Feb  6 2013 Darryl L. Pierce <dpierce@redhat.com> - 2.0.4-1
- Rebased on release 2.0.4.

* Mon Jan  7 2013 Darryl L. Pierce <dpierce@redhat.com> - 2.0.3-3.2
- Fixed the name of the installed gem.

* Thu Dec 20 2012 Darryl L. Pierce <dpierce@redhat.com> - 2.0.3-3.1
- Cleaned up the specfile to match current Ruby packaging guidelines.
- Changed URL to point to Dominik Honnef's project page on his blog.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Darryl L. Pierce <dpierce@redhat.com> - 2.0.3-2
- First official release for Fedora.

* Sun Jul  8 2012 Darryl L. Pierce <dpierce@redhat.com> - 2.0.3-1.1
- Removed ruby and ruby(abi) BuildRequires.
- Removed ruby Requires.

* Thu Jun 28 2012 Darryl L. Pierce <dpierce@redhat.com> - 2.0.3-1
- Initial package
