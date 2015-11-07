%global	gem_name	mini_portile

Name:		rubygem-%{gem_name}
Version:	0.6.2
Release:	4%{?dist}
Summary:	Simplistic port-like solution for developers
Group:		Development/Languages
License:	MIT

URL:		http://github.com/flavorjones/mini_portile
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
Requires:	ruby(release)
Requires:	ruby(rubygems)
BuildArch:	noarch

Provides: rubygem(%{gem_name}) = %{version}-%{release}

%description
Simplistic port-like solution for developers. It provides a standard and
simplified way to compile against dependency libraries without messing up
your system.


%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

# Permission
find . -name \*.rb -print0 | xargs --null chmod 0644

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile
%{gem_libdir}/

%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}/
# Currently no useful
%exclude	%{gem_instdir}/examples/

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.6.2-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.6.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 31 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.1-1
- 0.6.2

* Wed Aug 13 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.1-1
- 0.6.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.0-1
- 0.6.0

* Mon Apr 07 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.3-1
- 0.5.3

* Tue Oct 29 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.2-1
- 0.5.2

* Sun Jul 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.1-1
- Initial package
