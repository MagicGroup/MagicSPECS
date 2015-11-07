%global gem_name spring

Name: rubygem-%{gem_name}
Version: 1.3.6
Release: 4%{?dist}
Summary: Rails application preloader
Group: Development/Languages
License: MIT
URL: http://github.com/rails/spring
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rails/spring.git && cd spring
# git checkout v1.3.6 && tar czvf rubygem-spring-1.3.6-tests.tar.gz ./test
Source1: rubygem-spring-1.3.6-tests.tar.gz
Requires: ruby(release)
Requires: ruby(rubygems)
# Needed by `spring status`
Requires: %{_bindir}/ps
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(bundler)
BuildRequires: rubygem(activesupport)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}
# OkJson is allowed to be bundled:
# https://fedorahosted.org/fpc/ticket/113
Provides: bundled(okjson) = 43

%description
Spring is a Rails application preloader. It speeds up development by keeping
your application running in the background so you don't need to boot it every
time you run a test, rake task or migration.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
tar xf %{SOURCE1}

# Run only unit test now, acceptance tests wants to compile gems extensions
ruby -Ilib:test -rspring/watcher -e 'Dir.glob "./test/unit/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{_bindir}/spring
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/test/apps/.gitignore
%{gem_spec}
%doc %{gem_instdir}/LICENSE.txt

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.3.6-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.3.6-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Josef Stribny <jstribny@redhat.com> - 1.3.6-1
- Update to 1.3.6

* Wed Jul 09 2014 Josef Stribny <jstribny@redhat.com> - 1.1.3-1
- Update to 1.1.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Josef Stribny <jstribny@redhat.com> - 1.1.2-4
- Use macro for the ps bin path

* Thu Mar 20 2014 Josef Stribny <jstribny@redhat.com> - 1.1.2-3
- Fix ps require

* Tue Mar 18 2014 Josef Stribny <jstribny@redhat.com> - 1.1.2-2
- Add bundled okjson virtual provide
- Add ps dependency
- Exclude .gitignore from tests

* Fri Mar 14 2014 Josef Stribny <jstribny@redhat.com> - 1.1.2-1
- Initial package
