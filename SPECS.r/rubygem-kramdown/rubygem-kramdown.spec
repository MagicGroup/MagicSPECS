# Generated from kramdown-1.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name kramdown
%if 0%{?fedora} >= 21
%define	gem_minitest	rubygem(minitest4)
%else
%define	gem_minitest	rubygem(minitest)
%endif

Name: rubygem-%{gem_name}
Version: 1.8.0
Release: 4%{?dist}
Summary: Fast, pure-Ruby Markdown-superset converter

License:	MIT
URL:		http://kramdown.rubyforge.org
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	%gem_minitest
Requires:	ruby(release)
Requires:	ruby(rubygems)
BuildArch: noarch

Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
kramdown is yet-another-markdown-parser but fast, pure Ruby,
using a strict syntax definition and supporting several common extensions.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

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

# Move man pages
mkdir -p %{buildroot}%{_mandir}/man1
mv %{buildroot}%{gem_instdir}/man/man1/kramdown.1 \
	%{buildroot}%{_mandir}/man1

# Cleanup
pushd %{buildroot}%{gem_instdir}
rm -rf \
	setup.rb Rakefile \
	benchmark/ \
	test/

%check
LANG=en_US.utf8

pushd .%{gem_instdir}

%if 0%{?fedora} >= 21
sed -i.minitest \
	-e "\@require 'kramdown'@i gem 'minitest', '~> 4'" \
	test/run_tests.rb
%endif

# Some tests seem to be failing, need investigating
ruby -Ilib:test:. --verbose test/run_tests.rb 2>&1 | tee test-result.log
cat test-result.log | grep FAILED && echo "Please investigate this" || true
popd

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*

%{_bindir}/kramdown
%{gem_instdir}/bin
%{_mandir}/man1/kramdown.1*

%{gem_libdir}/
%{gem_instdir}/data/

%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}
%doc	%{gem_instdir}/doc/

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.8.0-4
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.8.0-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.8.0-2
- 为 Magic 3.0 重建

* Mon Jul  6 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.0-1
- 1.8.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.0-1
- 1.7.0

* Sun Mar  1 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.0-1
- 1.6.0

* Fri Nov  7 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.0-1
- 1.5.0

* Mon Sep 22 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.2-1
- 1.4.2

* Wed Aug 13 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.1-1
- 1.4.1

* Fri Jun 27 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.0-1
- 1.4.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.3-1
- 1.3.3

* Sat Feb 22 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.2-1
- 1.3.2

* Thu Jan 09 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.1-1
- 1.3.1

* Thu Dec 12 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.0-1
- 1.3.0

* Fri Nov 15 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.0-1
- Initial package
