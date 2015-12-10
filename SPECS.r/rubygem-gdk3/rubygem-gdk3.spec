%global	header_dir	%{ruby_vendorarchdir}
%global	gem_name	gdk3
%global	glib_min_ver	2.2.4

# Planned for F-20+ only
Summary:	Ruby binding of GDK-3.x
Name:		rubygem-%{gem_name}
Version:	2.2.5
Release:	5%{?dist}

Group:		Development/Languages
# Various files in gem
License:	LGPLv2+
URL:		http://ruby-gnome2.sourceforge.jp/
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://raw.github.com/ruby-gnome2/ruby-gnome2/master/gdk3/COPYING.LIB
# Renamed to avoid overwrite on SOURCE dir
Source1:	COPYING.LIB.gdk3

# MRI only
Requires:	ruby
BuildRequires:	ruby

Requires:	ruby(rubygems) 
# FIXME it seems this is needed
Requires:	rubygem(atk)
BuildRequires:	ruby-devel
BuildRequires:	rubygems-devel
BuildRequires:	rubygem-glib2-devel >= %{glib_min_ver}
BuildRequires:	rubygem-pango-devel
BuildRequires:	gtk3-devel
# %%check
BuildRequires:	rubygem(gdk_pixbuf2)
BuildRequires:	rubygem(cairo-gobject)
BuildRequires:	rubygem(gobject-introspection)
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(test-unit-notify)
# FIXME it seems this is needed
BuildRequires:	rubygem(atk)
# X is needed
BuildRequires:	xorg-x11-server-Xvfb
Provides:	rubygem(%{gem_name}) = %{version}-%{release}
Obsoletes:		rubygem-gdk3-devel < 2.2.3
# BuildArch changed from 2.2.3
BuildArch:		noarch

%description
Ruby/GDK3 is a Ruby binding of GDK-3.x.

%package	devel
Summary:	Ruby/GLib development environment
Group:		Development/Languages
Requires:	%{name}%{?isa} = %{version}-%{release}
Requires:	gtk3-devel%{?isa}
Requires:	ruby-devel%{?isa}

%description devel
Header files and libraries for building a extension library for the
rubygem-%{gem_name}

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

# Allow ruby-gnome2 no less than ones
sed -i -e 's|= 2\.2\.5|>= 2.2.5|' %{gem_name}.gemspec

# Add license text
install -cpm 644 %{SOURCE1} ./COPYING.LIB
sed -i -e '/files =/s|\("Rakefile",\)|\1 "COPYING.LIB", |' \
	%{gem_name}.gemspec

gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
mkdir -p .%{gem_dir}

export CONFIGURE_ARGS="--with-cflags='%{optflags} -Werror-implicit-function-declaration'"
export CONFIGURE_ARGS="$CONFIGURE_ARGS --with-pkg-config-dir=$(pwd)%{_libdir}/pkgconfig"
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# move header files, C extension files to the correct directory
%if 0
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a ./%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

pushd %{buildroot}
mkdir -p .%{header_dir}
mv .%{gem_extdir_mri}/*.h .%{header_dir}/
rm -f .%{gem_extdir_mri}/{gem_make.out,mkmf.log}
popd


# move pkgconfig file
mkdir %{buildroot}%{_libdir}/pkgconfig
install -cpm 644 ./%{_libdir}/pkgconfig/*.pc \
	%{buildroot}%{_libdir}/pkgconfig/
%endif

# Cleanups
pushd %{buildroot}
rm -rf .%{gem_instdir}/ext/
rm -f .%{gem_instdir}/extconf.rb
popd

%check
pushd .%{gem_instdir}

# kill unneeded make process
rm -rf ./TMPBINDIR
mkdir ./TMPBINDIR
pushd ./TMPBINDIR
ln -sf /bin/true make
export PATH=$(pwd):$PATH
popd

xvfb-run \
	ruby -Ilib:test:ext/%{gem_name} ./test/run-test.rb

popd


%files
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile
%dir	%{gem_instdir}/
%dir	%{gem_instdir}/lib/
%{gem_instdir}/lib/%{gem_name}.rb
%dir	%{gem_instdir}/lib/%{gem_name}/
%{gem_instdir}/lib/%{gem_name}/*.rb

%if 0
%{gem_extdir_mri}/
%endif

%exclude %{gem_cache}
%{gem_spec}

%if 0
%files	devel
%{_libdir}/pkgconfig/ruby-%{gem_name}.pc
%{header_dir}/rbgdk3.h
%{header_dir}/rbgdk3conversions.h
%endif

%files	doc
%doc	%{gem_docdir}/
%exclude	%{gem_instdir}/test/

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.2.5-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.2.5-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.2.5-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.5-1
- 2.2.5

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.4-1
- Define arch as noarch (bug 1161947)

* Wed Nov  5 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.3-1
- 2.2.3

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-2
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Mon Apr 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-1
- 2.2.0

* Wed Feb 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.0-2
- Apply upstream patch to make GdkEventButton inherit GdkEventAny

* Thu Jan 16 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.0-1
- 2.1.0

* Thu Sep 19 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.2-2
- Patch from upstream to fix TestGdkRGBA

* Sun Aug 25 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.2-1
- 2.0.2

* Mon Apr 29 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.6-1
- 1.2.6

* Fri Mar 22 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.3-1
- 1.2.3

* Mon Feb 18 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.1-1
- Initial package
