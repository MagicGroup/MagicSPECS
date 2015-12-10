# Generated from jbuilder-1.5.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name jbuilder

%global bootstrap 0

Name: rubygem-%{gem_name}
Version: 2.3.0
Release: 4%{?dist}
Summary: Create JSON structures via a Builder-style DSL
Group: Development/Languages
License: MIT
URL: https://github.com/rails/jbuilder
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fix: Properly require ostruct
# https://github.com/rails/jbuilder/pull/281
Patch0: rubygem-jbuilder-ostruct.patch
BuildRequires: ruby(release)
%if 0%{bootstrap} < 1
BuildRequires: rubygem(minitest) >= 5.0.0
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(rails)
BuildRequires: rubygem(multi_json)
%endif
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Jbuilder gives you a simple DSL for declaring JSON structures that beats
massaging giant hash structures. This is particularly helpful when
the generation process is fraught with conditionals and loops.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
%if 0%{bootstrap} < 1
pushd .%{gem_instdir}
# Get rid of Bundler
sed -i -e '1d' test/test_helper.rb
rm Gemfile
ruby -rshellwords -Ilib:test -e "Dir.glob './test/*_test.rb', &method(:require)"
popd
%endif


%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%doc %{gem_instdir}/MIT-LICENSE
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/test
%{gem_instdir}/gemfiles
%{gem_instdir}/Appraisals

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.3.0-4
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.3.0-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.3.0-2
- 为 Magic 3.0 重建

* Mon Jun 29 2015 Josef Stribny <jstribny@redhat.com> - 2.3.0-1
- Update to 2.3.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Josef Stribny <jstribny@redhat.com> - 2.2.12-1
- Update to 2.2.12

* Tue Oct 14 2014 Josef Stribny <jstribny@redhat.com> - 2.2.2-1
- Update to 2.2.2

* Mon Aug 18 2014 Josef Stribny <jstribny@redhat.com> - 2.1.3-1
- Update to 2.1.3

* Wed Jul 09 2014 Josef Stribny <jstribny@redhat.com> - 2.1.1-1
- Update to 2.1.1

* Thu Jun 12 2014 Josef Stribny <jstribny@redhat.com> - 2.1.0-1
- Update to jbuilder 2.1.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 07 2014 Josef Stribny <jstribny@redhat.com> - 2.0.4-1
- Update to jbuilder 2.0.4

* Tue Jul 30 2013 Josef Stribny <jstribny@redhat.com> - 1.5.0-1
- Initial package
