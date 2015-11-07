%global	header_dir	%{ruby_vendorarchdir}

%global	gem_name		cairo
%global	gemver		1.14.3
#%%global	gem_githash	af3e3fc059

# Upstream GIT http://github.com/rcairo/

Summary:	Ruby bindings for cairo
Name:		rubygem-%{gem_name}
Version:	%{gemver}
Release:	3%{?dist}
Group:		Development/Languages
License:	GPLv2 or Ruby
URL:		http://cairographics.org/rcairo/
%if 1
Source0:	http://rubygems.org/downloads/%{gem_name}-%{version}.gem
%else
Source0:	%{gem_name}-%{gemver}-%{gem_githash}.gem
%endif
# Git based gem is created by below
Source1:	create-cairo-gem.sh

%if 0%{?fedora} >= 19
Requires:	ruby(release)
BuildRequires:	ruby(release)
%else
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby 
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby 
%endif

BuildRequires:	rubygems-devel
BuildRequires:	cairo-devel
BuildRequires:	ruby-devel
# For %%check
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(test-unit-notify)
BuildRequires:	rubygem(pkg-config)
# Make sure at least one font is available for test/test_context.rb:57
# `initialize': out of memory (NoMemoryError)
BuildRequires:	dejavu-serif-fonts
Requires:	rubygems
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

Obsoletes:	ruby-%{gem_name} <= %{version}-%{release}
Provides:	ruby-%{gem_name} = %{version}-%{release}

%description
Ruby bindings for cairo. Cairo is a 2D graphics library with support for 
multiple output devices. Currently supported output targets include the 
X Window System, win32, and image buffers.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%package	devel
Summary:	Ruby-cairo development environment
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	cairo-devel
Requires:	ruby-devel
# Obsoletes / Provides
# ruby(cairo-devel) Provides is for compatibility
#
# Actually ruby(cairo-devel) provides should not exist -
# Remove on F-17 and above
Obsoletes:	ruby-cairo-devel < 1.9
Provides:	ruby-cairo-devel = %{version}-%{release}

%description devel
Header files and libraries for building a extension library for the
ruby-cairo

%prep
%setup -q -T -c

mkdir -p ./%{gem_dir}
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
%gem_install -n %{SOURCE0}

find . -name \*.gem | xargs chmod 0644

%build
# pkg-config dependency should be for development
find . -name \*.gemspec | \
	xargs sed -i -e '\@pkg-config@s|runtime_dependency|development_dependency|'

# Once install to TMPINSTDIR for %%check
rm -rf ./TMPINSTDIR
mkdir -p ./TMPINSTDIR/%{gem_dir}
cp -a ./%{gem_dir}/* ./TMPINSTDIR/%{gem_dir}

TOPDIR=$(pwd)

## remove all shebang, set permission to 0644
for f in $(find ./TMPINSTDIR/%{gem_instdir} -name \*.rb)
do
	sed -i -e '/^#!/d' $f
	chmod 0644 $f
done

# Move C extension
%if 0%{?fedora} >= 21
mkdir -p ./TMPINSTDIR/%{gem_extdir_mri}
cp -a ./%{gem_extdir_mri}/*  TMPINSTDIR/%{gem_extdir_mri}/

pushd ./TMPINSTDIR
mkdir -p .%{header_dir}
mv .%{gem_extdir_mri}/*.h .%{header_dir}/
rm -f .%{gem_extdir_mri}/{gem_make.out,mkmf.log}

popd

%else
pushd ./TMPINSTDIR
mkdir -p .%{gem_extdir_mri}/lib
mv .%{gem_instdir}/lib/%{gem_name}.so \
	./%{gem_extdir_mri}/lib

# Move header
mkdir -p ./%{header_dir}
mv ./%{gem_instdir}/lib/*.h \
	./%{header_dir}/
popd
%endif


# cleanups
rm -rf ./TMPINSTDIR/%{gem_instdir}/ext/
rm -f ./TMPINSTDIR/%{gem_instdir}/{Makefile*,extconf.rb}

%install
cp -a ./TMPINSTDIR/* %{buildroot}/

%check
%if 0%{?fedora} >= 21
export RUBYLIB=$(pwd)/TMPINSTDIR/%{gem_instdir}:$(pwd)/TMPINSTDIR/%{gem_extdir_mri}/
%else
export RUBYLIB=$(pwd)/TMPINSTDIR/%{gem_instdir}:$(pwd)/TMPINSTDIR/%{gem_extdir_mri}/lib
%endif

pushd ./TMPINSTDIR/%{gem_instdir}
# kill unneeded make process
rm -rf ./TMPBINDIR
mkdir ./TMPBINDIR
pushd ./TMPBINDIR
ln -sf /bin/true make
export PATH=$(pwd):$PATH
popd

# Fix up test/run-test.rb
sed -i -e '\@require .rubygems@a\\ngem "test-unit"\n' test/run-test.rb
sed -i -e "\@require 'bundler/setup'@d" test/run-test.rb

ruby ./test/run-test.rb
popd

%files
%if 0%{?fedora} >= 21
%{gem_extdir_mri}/
%else
%dir %{gem_extdir_mri}
%dir %{gem_extdir_mri}/lib
%{gem_extdir_mri}/lib/%{gem_name}.so
%endif

%dir	%{gem_instdir}/
%doc	%{gem_instdir}/[A-Z]*
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Rakefile
%{gem_instdir}/lib/
%if 0%{?fedora} >= 20
%exclude	%{gem_cache}
%else
%{gem_cache}
%endif
%{gem_spec}

%files	doc
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/samples/
%{gem_instdir}/test/
%{gem_docdir}/

%files	devel
%{header_dir}/rb_cairo.h

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.14.3-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.14.3-2
- 为 Magic 3.0 重建

* Wed Sep  9 2015 amoru TASAKA <mtasaka@fedoraproject.org> - 1.14.3-1
- 1.14.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 15 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.1-2
- F-22: Rebuild for ruby 2.2

* Fri Dec 26 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.1-1
- 1.14.1

* Tue Nov 25 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.0-1
- 1.14.0

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.9-2
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Wed Apr  9 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.9-1
- 1.12.9

* Mon Dec 30 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.8-1
- 1.12.8

* Tue Aug  6 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.6-1
- 1.12.6

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Mamoru TASAKA <mtasaka@fedoraproject.org>
- Rebuild due to wrong %%gem_extdir_mri macro (bug 927471)

* Tue Mar 19 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.4-1
- 1.12.4

* Sun Mar  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.3-3
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct  6 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.3-1
- 1.12.3

* Thu Sep  6 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.12.2-1
- Update to 1.12.2 formal

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.2-0.2.gitaf3e3fc059
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.12.2-0.1.gitaf3e3fc059
- Update to 1.12.1
- And use git based gem for now to avoid test failure

* Tue Apr 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.10.2-4
- Fix conditionals for F17 to work for RHEL 7 as well.

* Sun Jan 29 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.10.2-3
- F-17: rebuild against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.10.2-1
- 1.10.2
- Make dependency for pkg-config be development only again
- Change the license tag to "GPLv2 or Ruby"
- Remove defattr

* Sun Oct 16 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.10.1-1
- 1.10.1

* Mon Feb 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.10.0-4
- F-15 mass rebuild
- Ignore test failure for now

* Sun Oct 31 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.10.0-3
- Move C extension so that "require %%gem_name" works correctly

* Tue Oct  5 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.10.0-2
- Install one font at BuildRequires for test	

* Sun Sep 19 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.10.0-1
- Update to 1.10.0

* Fri Sep  3 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.8.5-2
- Switch to gem
- Fix license tag

* Thu Sep  2 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.8.5-1
- Update to 1.8.5

* Wed Dec 16 2009 Allisson Azevedo <allisson@gmail.com> 1.8.1-1
- Update to 1.8.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Allisson Azevedo <allisson@gmail.com> 1.8.0-2
- Rebuild

* Sun Oct  5 2008 Allisson Azevedo <allisson@gmail.com> 1.8.0-1
- Update to 1.8.0

* Tue Sep  9 2008 Allisson Azevedo <allisson@gmail.com> 1.7.0-1
- Update to 1.7.0

* Sun May 18 2008 Allisson Azevedo <allisson@gmail.com> 1.6.1-1
- Update to 1.6.1

* Mon Feb 25 2008 Allisson Azevedo <allisson@gmail.com> 1.5.1-1
- Update to 1.5.1
- Update License for GPLv2+

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.0-2
- Autorebuild for GCC 4.3

* Mon Jun 11 2007 Allisson Azevedo <allisson@gmail.com> 1.5.0-1
- Update to 1.5.0

* Sun Mar 28 2007 Allisson Azevedo <allisson@gmail.com> 1.4.1-2
- Changed license for Ruby License/GPL
- Add ruby-devel for devel requires
- Changed main group for System Environment/Libraries
- Changed install for keep timestamps

* Sun Mar 26 2007 Allisson Azevedo <allisson@gmail.com> 1.4.1-1
- Initial RPM release
