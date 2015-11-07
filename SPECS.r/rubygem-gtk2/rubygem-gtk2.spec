%global	header_dir	%{ruby_vendorarchdir}

%global	gem_name	gtk2

%global	glibminver	2.2.5
%global	pangominver	%{glibminver}
%global	obsoleteevr	0.90.7-1.999

Summary:	Ruby binding of GTK+-2.x
Name:		rubygem-%{gem_name}
Version:	2.2.5
Release:	4%{?dist}
Group:		Development/Languages
# from README
License:	LGPLv2
URL:		http://ruby-gnome2.sourceforge.jp/
Source0:	http://rubygems.org/downloads/%{gem_name}-%{version}.gem

Requires:	ruby(release)
BuildRequires:	ruby(release)

BuildRequires:	rubygems-devel
BuildRequires:	rubygem-cairo-devel >= 1.2.5
BuildRequires:	rubygem-glib2-devel >= %{glibminver}
BuildRequires:	rubygem-pango-devel >= %{pangominver}
BuildRequires:	ruby-devel
BuildRequires:	gtk2-devel
BuildRequires:	rubygem(atk) >= %{glibminver}
BuildRequires:	rubygem(gdk_pixbuf2)
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(test-unit-notify)
# %%check
# Testsuite needs X
BuildRequires:	xorg-x11-server-Xvfb
# Icon for face-cool
BuildRequires:	gnome-icon-theme
# gtkrc
BuildRequires:	adwaita-gtk2-theme
# "actions/find"
BuildRequires:	gnome-icon-theme-legacy
Requires:	rubygems
Provides:	rubygem(%{gem_name}) = %{version}

Obsoletes:	ruby-%{gem_name} = %{version}-%{release}
Provides:	ruby-%{gem_name} = %{version}-%{release}
Provides:	ruby(%{gem_name}) = %{version}-%{release}

%description
Ruby/GTK2 is a Ruby binding of GTK+-2.0.x.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%package	-n ruby-%{gem_name}
Summary:	Non-Gem support package for %{gem_name}
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
# Requires for corresponsing non-gem rpms
Requires:	ruby(atk) >= %{glibminver}
Requires:	ruby(gdk_pixbuf2) >= %{glibminver}
Requires:	ruby(glib2) >= %{glibminver}
Requires:	ruby(pango) >= %{glibminver}
Provides:	ruby(%{gem_name}) = %{version}-%{release}

%description	-n ruby-%{gem_name}
This package provides non-Gem support for %{gem_name}.

%package	devel
Summary:	Ruby/GTK development environment
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	ruby-devel
Requires:	gtk2-devel
Requires:	rubygem-glib2-devel
# Obsoletes / Provides
# ruby(%%{gem_name}-devel) Provides is for compatibility
Obsoletes:	ruby-%{gem_name}-devel < %{obsoleteevr}
Provides:	ruby-%{gem_name}-devel = %{version}-%{release}

%description devel
Header files and libraries for building a extension library for the
rubygem-%{gem_name}

%prep
%setup -q -c -T
mkdir -p .%{gem_dir}

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec

# Allow ruby-gnome2 no less than ones
sed -i -e 's|= 2\.2\.5|>= 2.2.5|' %{gem_name}.gemspec

# Patches and etc

# Fix wrong dir
grep -rl /usr/local/bin sample | \
	xargs sed -i -e 's|/usr/local/|/usr/|'

# Kill shebang
grep -rl '#!.*/usr/bin' sample lib | \
	xargs sed -i -e '\@#![ ]*/usr/bin@d'
find sample/ -name \*.rb | xargs chmod 0644

# Repackage gem
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
export CONFIGURE_ARGS="$CONFIGURE_ARGS --with-pkg-config-dir=$(pwd)%{_libdir}/pkgconfig"
%gem_install

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
mkdir -p .%{header_dir}
mv .%{gem_extdir_mri}/*.h .%{header_dir}/
rm -f .%{gem_extdir_mri}/{gem_make.out,mkmf.log}
popd


# move pkgconfig file
mkdir %{buildroot}%{_libdir}/pkgconfig
install -cpm 644 ./%{_libdir}/pkgconfig/*.pc \
	%{buildroot}%{_libdir}/pkgconfig/


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

%files
%defattr(-,root,root,-)
%dir	%{gem_instdir}
%dir	%{gem_instdir}/lib/
%dir	%{gem_instdir}/lib/%{gem_name}/

%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile

%{gem_instdir}/lib/%{gem_name}.rb
%{gem_instdir}/lib/%{gem_name}/base.rb
%{gem_extdir_mri}/

%exclude	%{gem_cache}
%{gem_spec}

%files	devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/ruby-%{gem_name}.pc
%{header_dir}/rbgdk.h
%{header_dir}/rbgdkconversions.h
%{header_dir}/rbgtk.h
%{header_dir}/rbgtkconversions.h
%{header_dir}/rbgtkmacros.h

%files	doc
%defattr(-,root,root,-)
%{gem_dir}/doc/%{gem_name}-%{version}
%exclude	%{gem_instdir}/Rakefile
%{gem_instdir}/sample/
%{gem_instdir}/test/

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.2.5-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.2.5-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.5-1
- 2.2.5

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.4-2
- F-22: Rebuild for ruby 2.2

* Sun Dec 28 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.4-1
- 2.2.4

* Wed Nov  5 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.3-1
- 2.2.3

* Sun Oct 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-5
- Fix test_type_integer(TestSelectionData) test failure
  on bigendian + 64bit (ppc64, s390x) (bug 1149702)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-2
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Mon Apr 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-1
- 2.2.0

* Tue Feb 11 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.0-2
- Apply upstream patch to make GdkEventButton inherit GdkEventAny

* Thu Jan 16 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.0-1
- 2.1.0

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.2-1
- 2.0.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 17 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.6-1
- 1.2.6

* Thu Apr  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.5-1
- 1.2.5

* Tue Mar 26 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.4-1
- 1.2.4

* Wed Mar 20 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.3-1
- 1.2.3

* Sun Mar  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.1-2
- F-19: Rebuild for ruby 2.0.0

* Mon Feb  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.1-1
- 1.2.1

* Wed Jan 30 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.0-1
- 1.2.0

* Mon Dec 31 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.9-1
- 1.1.9

* Thu Dec  6 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.6-1
- 1.1.6

* Wed Sep  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.5-1
- 1.1.5

* Mon Aug 13 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.4-1
- 1.1.4

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 16 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.3-1
- 1.1.3

* Tue Apr 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.2-4
- Fix conditionals for F17 to work for RHEL 7 as well.

* Wed Feb  1 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.2-3
- Add proper Obsoletes/Provides

* Tue Jan 31 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.2-2
- 1.1.2

* Sun Jan 15 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.1-1
- 1.1.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- F-17: Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 19 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.3-2
- 1.0.3

* Fri Jul 15 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.0-1
- 1.0.0

* Sun Jun 12 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.90.9-1
- 0.90.9

* Sat Mar  5 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.90.8-1
- 0.90.8

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  9 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.7-2
- 0.90.7

* Thu Nov 11 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.5-3
- Make ruby-gtk2 subpackage install corresponsing ruby- compat
  packages correctly (bug 652106)

* Sun Oct 31 2010 Mamoru Taska  <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.5-2
- 0.90.5
- Move C extension so that "require %%gem_name" works correctly

* Sun Oct 24 2010 Mamoru Taska  <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.4-2
- 0.90.4

* Sun Oct 24 2010 Mamoru Taska  <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.3-2
- 0.90.3

* Fri Oct  1 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.2-3
- Initial package
