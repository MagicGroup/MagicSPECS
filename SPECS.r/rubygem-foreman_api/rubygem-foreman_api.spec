%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name foreman_api

%if 0%{?rhel} == 6
%define rubyabi 1.8
%endif

Summary: Ruby bindings for Forman's rest API
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.1.11
Release: 5%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/theforeman/foreman_api
Source0:  http://rubygems.org/downloads/%{gem_name}-%{version}.gem
%if 0%{?fedora}
Requires: %{?scl_prefix}ruby(release)
%else
Requires: %{?scl_prefix}ruby(abi) = %{rubyabi}
%endif
Requires: %{?scl_prefix}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(json)
Requires: %{?scl_prefix}rubygem(rest-client) >= 1.6.1
Requires: %{?scl_prefix}rubygem(oauth)
%if 0%{?fedora}
BuildRequires: %{?scl_prefix}ruby(release)
%else
BuildRequires: %{?scl_prefix}ruby(abi) = %{rubyabi}
%endif
BuildRequires: %{?scl_prefix}ruby(rubygems)
BuildRequires: %{?scl_prefix}rubygems-devel

BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Helps you to use Foreman's API calls from your app.

%package doc
BuildArch:  noarch
Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
%{?scl:scl enable %{scl} "}
gem unpack %{SOURCE0}
%{?scl:"}
%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} "}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:"}
%{?scl:scl enable %{scl} "}
gem build %{gem_name}.gemspec
%{?scl:"}

%build
%if 0%{?fedora} > 18
%gem_install
%else
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} "}
gem install --local --install-dir .%{gem_dir} \
            --force --no-rdoc --no-ri %{gem_name}-%{version}.gem
%{?scl:"}
%endif

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
mv %{buildroot}%{gem_instdir}/{MIT-LICENSE,README.rdoc} ./
mkdir -p %{buildroot}%{gem_docdir}
mv %{buildroot}%{gem_instdir}/doc %{buildroot}%{gem_docdir}
rm -f %{buildroot}%{gem_instdir}/%{gem_name}.gemspec
rm -f %{buildroot}%{gem_instdir}/.yardopts
rm -f %{buildroot}%{gem_instdir}/.gitignore

%files
%dir %{gem_instdir}
%{gem_instdir}/lib
%exclude %{gem_cache}
%{gem_spec}

%doc MIT-LICENSE README.rdoc

%files doc
%doc %{gem_docdir}

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.1.11-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.1.11-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 11 2014 Miroslav Suchý <msuchy@redhat.com> 0.1.11-1
- rebase to foreman_api-0.1.11

* Sat Dec 21 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.9-2
- add scl macros
- clean up old unused code

* Sat Dec 21 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.9-1
- rebase to foreman_api-0.1.9

* Mon Nov 04 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.8-1
- rebase to 0.1.8

* Mon Oct 21 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.7-2
- rebase to 0.1.7
- updated api for hosts and media
* Mon Sep 02 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.6-1
- 1003399 - rebase to rubygem-foreman_api-0.1.6

* Fri Aug 23 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.5-2
- really add rebased gem

* Fri Aug 23 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.5-1
- rebase to 0.1.5

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.3-2
- 987286 - rebuild for F19

* Thu Apr 04 2013 Martin Bačovský <mbacovsk@redhat.com> 0.1.3-1
- Bump to 0.1.3 (mbacovsk@redhat.com)
- Fixed typo in logger (jhadvig@redhat.com)

* Thu Apr 04 2013 Martin Bačovský <mbacovsk@redhat.com> 0.1.2-2
- Removed .gitignore (mbacovsk@redhat.com)

* Wed Apr 03 2013 Martin Bačovský <mbacovsk@redhat.com> 0.1.2-1
- Bump to 0.1.2 (mbacovsk@redhat.com)

* Wed Apr 03 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.1-6
- 921985 - fix files section (msuchy@redhat.com)

* Fri Mar 15 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.1-5
- rebuild gem from source (msuchy@redhat.com)

* Fri Mar 15 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.1-4
- remove shebang from Rakefile (msuchy@redhat.com)

* Fri Mar 15 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.1-3
- mark Rakefile as executable (msuchy@redhat.com)

* Fri Mar 15 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.1-2
- prepare spec for Fedora 19 (msuchy@redhat.com)

* Wed Feb 13 2013 Martin Bačovský <mbacovsk@redhat.com> 0.1.1-1
- Bump to 0.1.1 (mbacovsk@redhat.com)
- Added support for extra options for restclient resource

* Wed Feb 06 2013 Martin Bačovský <mbacovsk@redhat.com> 0.1.0-1
- Updated to 0.1.0 (mbacovsk@redhat.com)
- Added support for API V2
- Removed unnecessary dependency on apipie-rails

* Thu Jan 24 2013 Martin Bačovský <mbacovsk@redhat.com> 0.0.11-1
- Updated to 0.0.11 (mbacovsk@redhat.com)
- generator is part of the package
- yard docs

* Tue Jan 15 2013 Martin Bačovský <mbacovsk@redhat.com> 0.0.10-1
- Fixed params handeling (mbacovsk@redhat.com)

* Fri Jan 11 2013 Martin Bačovský <mbacovsk@redhat.com> 0.0.9-1
- Bump to 0.0.9 (mbacovsk@redhat.com) ( compute_resource domain environment host
   common_parameter hostgroup image medium operating_system ptable 
   puppetclass role template_kind )


* Thu Nov 22 2012 Martin Bačovský <mbacovsk@redhat.com> 0.0.8-1
- Updated to 0.0.8 (mbacovsk@redhat.com)

* Thu Nov 22 2012 Martin Bacovsky <mbacovsk@redhat.com> 0.0.8-1
- support for full foreman API

* Wed Oct 17 2012 Ivan Necas <inecas@redhat.com> 0.0.7-2
- Fix apipie-rails dependency (inecas@redhat.com)

* Tue Oct 09 2012 Martin Bačovský <mbacovsk@redhat.com> 0.0.7-1
- Rebuilt with apipie 0.0.12 (mbacovsk@redhat.com)

* Tue Sep 11 2012 Martin Bačovský <mbacovsk@redhat.com> 0.0.6-1
- Updated to 0.0.6 (mbacovsk@redhat.com)
- support for subnets

* Tue Aug 28 2012 Martin Bačovský <mbacovsk@redhat.com> 0.0.5-1
- Updated bindings to 0.0.5 (mbacovsk@redhat.com)

* Tue Aug 14 2012 Martin Bačovský <mbacovsk@redhat.com> 0.0.4-2
- Updated to v 0.0.4 (mbacovsk@redhat.com)
- added domains, config_templates

* Tue Aug 14 2012 Martin Bačovský <mbacovsk@redhat.com> 0.0.2-1
- Updated gem to 0.0.2 (mbacovsk@redhat.com)

* Mon Aug 13 2012 Miroslav Suchý <msuchy@redhat.com> 0.0.1-4
- for rubyabi do s/1.9/1.9.1/ (msuchy@redhat.com)

* Mon Aug 13 2012 Martin Bačovský <mbacovsk@redhat.com> 0.0.1-3
- Fixed failing spec removal (mbacovsk@redhat.com)

* Mon Aug 13 2012 Martin Bačovský <mbacovsk@redhat.com> 0.0.1-2
- new package built with tito

* Wed Aug 08 2012 Martin Bacovsky <mbacovsk@redhat.com> - 0.0.1-1
- Initial package
