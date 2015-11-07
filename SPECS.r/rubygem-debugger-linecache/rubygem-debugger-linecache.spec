%global	gem_name	debugger-linecache

Name:		rubygem-%{gem_name}
Version:	1.2.0
Release:	5%{?dist}

Summary:	Read file with caching

# lib/linecache19.rb is GPLv2+, other files (license file) is MIT
# https://github.com/cldwalker/debugger-linecache/issues/9
License:	GPLv2+ and MIT
URL:		http://github.com/cldwalker/debugger-linecache
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
# Renamed to avoid name overlap
Source1:	GPLv2-rubygem-debugger-linecache
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(test-unit)
%if 0%{?fedora} <= 20
Requires:	ruby(release)
Requires:	ruby(rubygems)
%endif

BuildArch:		noarch

%description
Linecache is a module for reading and caching lines. This may be useful for
example in a debugger where the same lines are shown many times.


%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

find . -name \*.rb | xargs chmod ugo-x
grep -rl '#! */usr/bin' lib | xargs sed -i '\@#! */usr/bin@d'

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

install -cpm 0644 %{SOURCE1} %{buildroot}%{gem_instdir}/GPL

pushd %{buildroot}%{gem_instdir}
rm -rf \
	.travis.yml \
	Rakefile \
	*.gemspec \
	test/ \
	%{nil}

%check
pushd .%{gem_instdir}
ruby -Ilib:. -e \
	'gem "test-unit" ; Dir.glob("test/test-*.rb").each { |f| require f }' || true

# It seems that test_all_lnum_data needs reconsideration
ruby -Ilib:. -e \
	'gem "test-unit" ; Dir.glob("test/test-*.rb").each { |f| require f unless /test-lnum/ =~ f }'
popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/LICENSE.txt
%license	%{gem_instdir}/GPL
%doc	%{gem_instdir}/README.md
%doc	%{gem_instdir}/CHANGELOG.md

%{gem_libdir}/
%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}
%doc	%{gem_instdir}/CONTRIBUTING.md
%doc	%{gem_instdir}/OLD*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.2.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.0-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb  5 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.0-2
- Modify license tag

* Mon Feb  2 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.0-1
- Initial package
