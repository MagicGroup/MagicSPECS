%global gem_name literati

Name: rubygem-%{gem_name}
Version: 0.0.4
Release: 5%{?dist}
Summary: Render literate Haskell with Ruby
Group: Development/Languages
License: MIT
URL: https://github.com/jm/literati
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# This gem uses Test::Unit + contest by default. I've cherry-picked Minitest
# support as Patch0.
# This is proposed upstream as a part of https://github.com/jm/literati/pull/12
Patch0: rubygem-literati-0.0.4-minitest.patch
# Fix mocha.
# https://github.com/jm/literati/pull/13
Patch1: rubygem-literati-0.0.4-mocha.patch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Render literate Haskell with Ruby for great good.


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

# Remove developer-only file.
rm Rakefile
sed -i "s/\"Rakefile\",//g" %{gem_name}.gemspec

# Minitest support.
# https://github.com/jm/literati/pull/12
%patch0 -p1
sed -i "s/contest/minitest/g" %{gem_name}.gemspec
# Fix mocha.
# https://github.com/jm/literati/pull/13
%patch1 -p1

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove unnecessary gemspec
rm .%{gem_instdir}/%{gem_name}.gemspec

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
  ruby -I"lib" -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/LICENSE
%{_bindir}/literati
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/test

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.0.4-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jul 09 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.4-3
- Patch for mocha invocation

* Wed May 28 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.4-2
- Use HTTPS URL
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sat Dec 28 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.4-1
- Initial package
