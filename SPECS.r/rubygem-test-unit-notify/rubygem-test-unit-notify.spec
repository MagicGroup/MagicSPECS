%global	gem_name	test-unit-notify
%if 0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif

Summary:	Test::Unit::Notify - A test result notify extension for Test::Unit
Name:		rubygem-%{gem_name}
Version:	1.0.4
Release:	5%{?dist}
Group:		Development/Languages
# https://github.com/test-unit/test-unit-notify/issues/2
License:	LGPLv2+ and (LGPLv2+ or GFDL or CC-BY-SA)
URL:		http://rubyforge.org/projects/test-unit/
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem

%if 0%{?fedora} >= 19
Requires:	ruby(release)
BuildRequires:	ruby(release)
%else
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby 
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby 
%endif
Requires:	ruby(rubygems) 
Requires:	rubygem(test-unit)
BuildRequires:	rubygems-devel 
BuildArch:	noarch

Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
Test::Unit::Notify - A test result notify extension for Test::Unit.


%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
# Gem repack
TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}
gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

# Permission
find . -type f -print0 | xargs --null chmod go-w

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_instdir}/{Gemfile,Rakefile,.yardopts}

# No test suite available currently

%files
%dir	%{gem_instdir}
%{gem_instdir}/lib/
%{gem_instdir}/data/
%exclude	%{gem_cache}
%{gem_spec}

%doc	%{gem_instdir}/README.md
%doc	%{gem_instdir}/doc/

%files doc
%doc	%{gem_docdir}/
%doc	%{gem_instdir}/screenshot/

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.0.4-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.4-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.4-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Nov 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.4-1
- 1.0.4

* Wed Aug 13 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.3-1
- 1.0.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 15 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.1-1
- 1.0.1

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.3.0-3
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 04 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.3.0-1
- Initial package
