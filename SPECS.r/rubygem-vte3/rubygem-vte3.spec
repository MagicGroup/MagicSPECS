%global	gem_name	vte3
%global	glib_min_ver	2.2.5

Summary:	Ruby binding of VTE
Name:		rubygem-%{gem_name}
Version:	2.2.5
Release:	5%{?dist}

Group:		Development/Languages
License:	LGPLv2+
URL:		http://ruby-gnome2.sourceforge.jp/
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://raw.github.com/ruby-gnome2/ruby-gnome2/master/vte3/COPYING.LIB
# Renamed to avoid overwrite on SOURCE dir
Source1:	COPYING.LIB.vte3

BuildRequires:	vte3-devel
BuildRequires:	ruby-devel
BuildRequires:	rubygems-devel
BuildRequires:	rubygem-pango-devel
BuildRequires:	rubygem-gtk3-devel
BuildRequires:	rubygem-glib2-devel >= %{glib_min_ver}

%description
Ruby/VTE3 is a Ruby binding of VTE .

%package	devel
Summary:	Ruby/VTE3 development environment
Group:		Development/Languages
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for building a extension library for the
rubygem-%{gem_name} .

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name} .

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Relax the version dependency
sed -i -e 's|= 2\.2\.5|>= 2.2.5|' %{gem_name}.gemspec

# Add license text
install -cpm 644 %{SOURCE1} ./COPYING.LIB
sed -i -e '/files =/s|\("Rakefile",\)|\1 "COPYING.LIB", |' \
	%{gem_name}.gemspec

%build
export CONFIGURE_ARGS="--with-cflags='%{optflags} -Werror-implicit-function-declaration'"
export CONFIGURE_ARGS="$CONFIGURE_ARGS --with-pkg-config-dir=$(pwd)%{_libdir}/pkgconfig"
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# move header files, C extension files to the correct directory
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a ./%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

pushd %{buildroot}
rm -f .%{gem_extdir_mri}/{gem_make.out,mkmf.log}
popd

# move pkgconfig file
mkdir %{buildroot}%{_libdir}/pkgconfig
install -cpm 644 ./%{_libdir}/pkgconfig/*.pc \
	%{buildroot}%{_libdir}/pkgconfig/

# Cleanups
pushd %{buildroot}
rm -rf \
	.%{gem_instdir}/Rakefile \
	.%{gem_instdir}/extconf.rb \
	.%{gem_instdir}/ext/
popd

%check
# No test suite available yet

%files
%dir	%{gem_instdir}/
%license	%{gem_instdir}/COPYING.LIB
%dir	%{gem_instdir}/lib/
%{gem_instdir}/lib/%{gem_name}.rb
%dir	%{gem_instdir}/lib/%{gem_name}/
%{gem_instdir}/lib/%{gem_name}/*.rb

%{gem_extdir_mri}/

%exclude %{gem_cache}
%{gem_spec}

%files	devel
%{_libdir}/pkgconfig/ruby-%{gem_name}.pc

%files	doc
%doc	%{gem_docdir}/
%{gem_instdir}/sample/

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.2.5-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.2.5-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.2.5-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.5-1
- 2.2.5

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.4-3
- F-22: Rebuild for ruby 2.2

* Fri Jan 02 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.4-2
- Some cleanups

* Tue Dec 30 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.4-1
- Initial package
