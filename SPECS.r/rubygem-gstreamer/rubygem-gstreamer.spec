%global	header_dir	%{ruby_vendorarchdir}

%global		gem_name		gstreamer
%global		gemsoname		gst

%global		glibminver		2.2.5
%global		obsoleteevr	0.90.7-1.999


Summary:	Ruby binding of GStreamer
Name:		rubygem-%{gem_name}
Version:	2.2.5
Release:	2%{?dist}
Group:		Development/Languages
# from README
License:	LGPLv2
URL:		http://ruby-gnome2.sourceforge.jp/
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:	ruby(release)
BuildRequires:	ruby(release)

BuildRequires:	rubygems-devel
BuildRequires:	rubygem-glib2-devel >= %{glibminver}
BuildRequires:	rubygem-gobject-introspection-devel >= %{glibminver}
BuildRequires:	ruby-devel
BuildRequires:	pkgconfig(gstreamer-1.0)
# %%check
BuildRequires:	rubygem(test-unit)
# decodebin / playbin
BuildRequires:	gstreamer1-plugins-base

Provides:	rubygem(%{gem_name}) = %{version}-%{release}
# Kill non-gem support on F-17+
# Obsoletes but not provides
Obsoletes:	ruby-%{gem_name} < %{version}-%{release}

%description
Ruby/GStreamer is a Ruby binding of GStreamer.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%package	devel
Summary:	Ruby/GStreamer development environment
Group:		Development/Languages
Requires:	%{name}%{?_isa} = %{version}-%{release}
# Obsoletes / Provides
# ruby(%%{gem_name}-devel) Provides is for compatibility
# on F-15 and below
Obsoletes:	ruby-%{gem_name}-devel < %{obsoleteevr}

%description devel
Header files and libraries for building a extension library for the
rubygem-%{gem_name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Allow ruby-gnome2 no less than ones
sed -i -e 's|= 2\.2\.5|>= 2.2.5|' %{gem_name}.gemspec

# Fix wrong shebang
#grep -rl /usr/local/bin sample | \
#	xargs sed -i -e 's|/usr/local/bin|/usr/bin|'

# Kill shebang
grep -rl '#!.*/usr/bin' sample | \
	xargs sed -i -e '\@#![ ]*/usr/bin@d'
find sample/ -name \*.rb | xargs chmod 0644

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
mkdir -p %{buildroot}%{_libdir}/pkgconfig
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

ruby -Ilib:test:ext/%{gem_name} ./test/run-test.rb
popd


%files
%dir	%{gem_instdir}
%dir	%{gem_instdir}/lib/

%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile

%{gem_instdir}/lib/%{gemsoname}.rb
%{gem_instdir}/lib/%{gem_name}.rb
%{gem_instdir}/lib/%{gemsoname}/
%{gem_extdir_mri}/

%exclude	%{gem_cache}
%{gem_spec}

%files	devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/ruby-%{gem_name}.pc

%files	doc
%defattr(-,root,root,-)
%{gem_dir}/doc/%{gem_name}-%{version}
%exclude	%{gem_instdir}/Rakefile
%{gem_instdir}/sample/
%exclude	%{gem_instdir}/test/

%changelog
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

* Thu Mar  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.1-2
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

* Mon Apr 16 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.3-2
- 1.1.3

* Tue Jan 31 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.2-2
- 1.1.2

* Sun Jan 15 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.1-1
- 1.1.1

* Sat Dec 31 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.3-3
- Rescue test failure

* Thu Dec 29 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.3-2
- Add BR: gstreamer-plugins-good for smpte_caps in test/test_caps.rb
- Add BR: rubygem(test-unit)

* Wed Dec 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.3-1
- Initial package

