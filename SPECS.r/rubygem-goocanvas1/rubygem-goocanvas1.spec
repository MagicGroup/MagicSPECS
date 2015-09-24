%global	gem_name	goocanvas

%global	glibminver	2.0.0
%global	gtkminver	2.0.0

# Basically rubygems supports installation of multiple versions,
# (with gem "goocanvas", "~> 1.2"), so keep the original
# %%{gem_name} as much as possible - except for
# pkgconfig file

Summary:	Ruby binding of GooCanvas
Name:		rubygem-%{gem_name}1
Version:	1.2.6
Release:	7%{?dist}
Group:	Development/Languages
# from README
License:	LGPLv2
URL:		http://ruby-gnome2.sourceforge.jp/
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Licenses
# https://raw.github.com/ruby-gnome2/ruby-gnome2/master/COPYING.LIB
Source1:	COPYING.LIB.rubygem-goocanvas1
# http://www.gnu.org/licenses/gpl-2.0.txt
Source2:	COPYING.GPL.rubygem-goocanvas1

# CRuby only
Requires:	ruby
BuildRequires:	ruby

BuildRequires:	rubygems-devel
BuildRequires:	rubygem-cairo-devel
BuildRequires:	rubygem-gtk2-devel >= %{gtkminver}
BuildRequires:	rubygem-gdk_pixbuf2-devel >= %{gtkminver}
BuildRequires:	ruby-devel
BuildRequires:	goocanvas-devel
Requires:	ruby(rubygems)
Provides:	rubygem(%{gem_name}) = %{version}

%description
Ruby/GooCanvas is a Ruby binding of GooCanvas.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
# sample/demo.rb is under GPLv2+
License:	LGPLv2 and GPLv2+
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%package	devel
Summary:	Ruby/GooCanvas development environment
Group:		Development/Languages
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for building a extension library for the
rubygem-%{gem_name}

%prep
%setup -q -c -T
mkdir -p .%{gem_dir}

export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
export CONFIGURE_ARGS="$CONFIGURE_ARGS --with-pkg-config-dir=$(pwd)%{_libdir}/pkgconfig"
%gem_install -n %{SOURCE0}

find . -name \*.gem | xargs chmod 0644

pushd .%{gem_instdir}

# For rubygem-glib 2.0.x
sed -i \
	-e 's|GLib.prepend_environment_path|GLib.prepend_dll_path|' \
	lib/goocanvas.rb \
	sample/goocanvas-gi.rb

# Kill shebang
grep -rl '#!.*/usr/bin' sample | \
	xargs sed -i -e '\@#![ ]*/usr/bin@d'
find sample/ -name \*.rb | xargs chmod 0644
popd

%build
# Move C extension library to some private directory
pushd .%{gem_instdir}

%install
# Once copy all
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
# And rename this one (to avoid name conflict
# from rubygem-goocanvas)
mkdir %{buildroot}%{_libdir}/pkgconfig
install -cpm 644 ./%{_libdir}/pkgconfig/*.pc \
	%{buildroot}%{_libdir}/pkgconfig/ruby-%{gem_name}1.pc

# Cleanups
pushd %{buildroot}
rm -rf .%{gem_instdir}/ext/
rm -f .%{gem_instdir}/extconf.rb
popd

# Licenses
for f in %{SOURCE1} %{SOURCE2}
do
	install -cpm 644 $f %{buildroot}%{gem_instdir}/$(basename $f | sed -e 's|\.%{name}||')
done

%check
# Currently no testsuite available

%files
%dir	%{gem_instdir}
%dir	%{gem_instdir}/lib/

%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile

%{gem_instdir}/lib/%{gem_name}.rb
%{gem_extdir_mri}/

%exclude	%{gem_cache}
%{gem_spec}

%files	devel
%{_libdir}/pkgconfig/ruby-%{gem_name}1.pc

%files	doc
%{gem_docdir}/
%{gem_instdir}/Rakefile
%{gem_instdir}/sample/

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.6-6
- F-22: Rebuild for ruby 2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 21 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.6-3
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Fri Nov  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.6-2
- Incorporate comments on review request (bug 1025095)

* Thu Oct 31 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.6-1
- Initial package
