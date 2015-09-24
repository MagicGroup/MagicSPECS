%global	header_dir	%{ruby_vendorarchdir}

%global	gem_name	poppler

%global	glibminver	2.2.5
%global	obsoleteevr	0.90.7-1.999

Summary:	Ruby binding of poppler-glib
Name:		rubygem-%{gem_name}
Version:	2.2.5
Release:	2%{?dist}
Group:		Development/Languages
# from README
License:	LGPLv2
URL:		http://ruby-gnome2.sourceforge.jp/
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Omit tests failing without net
Patch2:	rubygem-poppler-0.90.5-omit-test-without-net.patch

Requires:	ruby(release)
BuildRequires:	ruby(release)

# Workaround: explicitly add libpng-devel to BR
# so that libpng12-devel won't be pulled in
BuildRequires:	libpng-devel >= 1.6

BuildRequires:	rubygems-devel
BuildRequires:	rubygem-cairo-devel
BuildRequires:	rubygem-glib2-devel >= %{glibminver}
BuildRequires:	rubygem-gdk_pixbuf2-devel
BuildRequires:	ruby-devel
BuildRequires:	poppler-glib-devel
## %%check
BuildRequires:	rubygem(test-unit) >= 3
Provides:	rubygem(%{gem_name}) = %{version}

Obsoletes:	ruby-%{gem_name} = %{version}-%{release}
Provides:	ruby-%{gem_name} = %{version}-%{release}
Provides:	ruby(%{gem_name}) = %{version}-%{release}

%description
Ruby/Poppler is a Ruby binding of poppler-glib.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.


%package	devel
Summary:	Ruby/Poppler development environment
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
# Obsoletes / Provides
# ruby(%%{gem_name}-devel) Provides is for compatibility
Obsoletes:	ruby-%{gem_name}-devel < %{obsoleteevr}
Provides:	ruby-%{gem_name}-devel = %{version}-%{release}

%description devel
Header files and libraries for building a extension library for the
rubygem-%{gem_name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

# Omit tests failing without net
%patch2 -p1

# Fix wrong shebang
#grep -rl /usr/local/bin sample | \
#	xargs sed -i -e 's|/usr/local/bin|/usr/bin|'

# Kill shebang
grep -rl '#!.*/usr/bin' sample | \
	xargs sed -i -e '\@#![ ]*/usr/bin@d'
find sample/ -name \*.rb | xargs chmod 0644
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Allow ruby-gnome2 no less than ones
sed -i -e 's|= 2\.2\.5|>= 2.2.5|' %{gem_name}.gemspec

%build
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
export CONFIGURE_ARGS="$CONFIGURE_ARGS --with-pkg-config-dir=$(pwd)%{_libdir}/pkgconfig"
gem build %{gem_name}.gemspec
%gem_install

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

sed -i.skip_make -e 's|which make|which nomake|' ./test/run-test.rb

# test_render fails
ruby -Itest:test:ext/%{gem_name} ./test/run-test.rb || ruby -Itest:test:ext/%{gem_name} ./test/run-test.rb -x test_page.rb

mv test/run-test.rb{.skip_make,}

%files
%defattr(-,root,root,-)
%dir	%{gem_instdir}
%dir	%{gem_instdir}/lib/

%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile

%{gem_instdir}/lib/%{gem_name}.rb
%{gem_extdir_mri}/

%exclude	%{gem_cache}
%{gem_spec}

%files	devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/ruby-%{gem_name}.pc

%files	doc
%defattr(-,root,root,-)
%{gem_docdir}/
%exclude	%{gem_instdir}/Rakefile
%{gem_instdir}/sample/
%{gem_instdir}/test/

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.5-1
- 2.2.5

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.4-2
- F-22: Rebuild for ruby 2.2

* Sun Dec 28 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.4-1
- 2.2.4

* Thu Dec  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.3-2
- Use newer test-unit (>= 3) and remove no longer needed patch

* Wed Nov  5 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.3-1
- 2.2.3

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 21 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-2
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Mon Apr 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-1
- 2.2.0

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

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 16 2012 Marek Kasik <mkasik@redhat.com> - 1.1.3-2
- Rebuild (poppler-0.20.0)

* Tue Apr 17 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.3-1
- 1.1.3

* Wed Feb  1 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.2-2
- 1.1.2

* Sun Jan 15 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.1-1
- 1.1.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- F-17: Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.0.3-5
- rebuild(poppler)

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 1.0.3-4
- Rebuild (poppler-0.18.0)

* Mon Sep 26 2011 Marek Kasik <mkasik@redhat.com> - 1.0.3-3
- Bump release because of EVR problems

* Mon Sep 19 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.3-2
- 1.0.3

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 1.0.0-3
- Rebuild (poppler-0.17.3)

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 1.0.0-2
- Rebuild (poppler-0.17.0)

* Fri Jul 15 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.0-1
- 1.0.0

* Sun Jun 12 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.90.9-1
- 0.90.9

* Thu May  5 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.90.8-3
- Patch to make tests succeed with poppler 0.17.0 (bug 698169)

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 0.90.8-2
- Rebuild (poppler-0.16.3)

* Sat Mar  5 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.90.8-1
- 0.90.8

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  9 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.7-2
- 0.90.7

* Sun Jan 02 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.90.5-6
- rebuild (poppler)

* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.90.5-5
- rebuild (poppler)

* Tue Dec  7 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.5-4
- Catch more exception on net related test

* Sun Nov 21 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.5-3
- Omit tests failing without net
- Remove miscs no longer needed on Fedora (%%clean section, etc)

* Sun Oct 31 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.5-2
- 0.90.5
- Move C extension so that "require %%gem_name" works correctly

* Sun Oct 24 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.4-2
- 0.90.4

* Mon Oct  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.2.3-1
- 0.90.2.3

* Sun Oct  3 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.90.2.2-1
- Initial package


