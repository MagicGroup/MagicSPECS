# This package contains macros that provide functionality relating to
# Software Collections. These macros are not used in default
# Fedora builds, and should not be blindly copied or enabled.
# Specifically, the "scl" macro must not be defined in official Fedora
# builds. For more information, see:
# http://docs.fedoraproject.org/en-US/Fedora_Contributor_Documentation
# /1/html/Software_Collections_Guide/index.html
%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name single_test

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.6.0
Release: 10%{?dist}
Summary: Rake tasks to invoke single tests/specs with rakish syntax
Group: Development/Languages
License: MIT
URL: http://github.com/grosser/single_test
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1: https://raw.github.com/grosser/single_test/master/MIT-LICENSE
Source2: https://raw.github.com/grosser/single_test/master/Readme.md 
%if 0%{?fedora} > 18
Requires: %{?scl_prefix}ruby(release)
%else
Requires: %{?scl_prefix}ruby(abi) = 1.9.1
%endif
Requires: %{?scl_prefix}ruby(rubygems) 
Requires: %{?scl_prefix}rubygem(rake) > 0.9
BuildRequires: %{?scl_prefix}rubygems-devel 
BuildRequires: %{?scl_prefix}rubygems
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Runs a single test/spec via rake.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%{?scl:scl enable %{scl} "}
gem unpack %{SOURCE0}
%{?scl:"}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} "}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:"}

cp -a %{SOURCE1} %{SOURCE2} ./

%build
mkdir -p .%{gem_dir}

# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} "}
gem build %{gem_name}.gemspec
%{?scl:"}

%{?scl:scl enable %{scl} - << \EOF}
%if 0%{?fedora} >= 18
%{gem_install}
%else
mkdir -p ./%{gem_dir}
gem install --local --install-dir ./%{gem_dir} --force %{gem_name}-%{version}.gem
%endif
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

chmod a-x %{buildroot}%{gem_libdir}/%{gem_name}/tasks.rb

for docfile in MIT-LICENSE Readme.md; do
  ln -s %{_pkgdocdir}/$docfile %{buildroot}%{gem_instdir}/
done

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc MIT-LICENSE Readme.md
%doc %{gem_instdir}/Readme.md
%doc %{gem_instdir}/MIT-LICENSE

%files doc
%doc %{gem_docdir}

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.6.0-10
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.6.0-9
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.6.0-8
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 30 2013 Miroslav Suchý <msuchy@redhat.com> 0.6.0-5
- fix readme file name

* Fri Aug 30 2013 Miroslav Suchý <msuchy@redhat.com> 0.6.0-4
- 1000334 - make symlink to README and LICENSE to pkgdocdir

* Tue Aug 27 2013 Miroslav Suchý <msuchy@redhat.com> 0.6.0-3
- add Readme and License

* Mon Aug 26 2013 Miroslav Suchý <msuchy@redhat.com> 0.6.0-2
- remove executable flag from tasks.rb
- remove BR rubygem-rspec
- use gem_install macro even for F18
- correct license (MIT)
- remove unused macro githash
- add comment about scl

* Fri Aug 23 2013 Miroslav Suchý <msuchy@redhat.com> 0.6.0-1
- rebase to 0.6.0

* Fri Aug 23 2013 Miroslav Suchý <msuchy@redhat.com> 0.5.2-3
- initial package

* Thu Jun 13 2013 Lukas Zapletal <lzap+git@redhat.com> 0.5.2-2
- post gem2rpm changes (lzap+git@redhat.com)

* Thu Jun 13 2013 Lukas Zapletal <lzap+git@redhat.com> 0.5.2-1
- new package built with tito

