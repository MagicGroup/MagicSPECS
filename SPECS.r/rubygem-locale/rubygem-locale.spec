# Upstream SCM:
# https://github.com/ruby-gettext/locale.git
%global	githash	bc30e1b7f820c458d825a43c2066ada339e99ffe
%global	shorthash	%(c=%{githash}; echo ${c:0:10})
%global	gitdate	Sat Oct 12 19:47:16 2013 +0900
%global	gitdate_num	20131012

%undefine	usegit
%global	mainrel	1

# Generated from locale-2.0.0.gem by gem2rpm -*- rpm-spec -*-
%if %{?fedora:0%{fedora} < 17}%{?rhel:0%{rhel} < 7}
%global	ruby_sitelib	%(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global	rubyabi	1.8
%global	ruby19	0
%else
%if 0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif
%global	ruby19	1
%endif

%global	gem_name	locale

%if 0%{?usegit} >= 1
%global	fedorarel	%{mainrel}.D%{gitdate_num}git%{shorthash}
%else
%global	fedorarel	%{mainrel}
%endif

Summary:	Pure ruby library which provides basic APIs for localization
Name:		rubygem-%{gem_name}
Version:	2.1.2
Release:	%{fedorarel}%{?dist}.2
Group:		Development/Languages
License:	GPLv2 or Ruby
URL:		http://locale.rubyforge.org/
%if	0%{?usegit} >= 1
Source0:	%{name}-%{version}-D%{gitdate_num}git%{shorthash}.tar.gz
%else
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
%endif

BuildArch:	noarch
BuildRequires:	ruby
Requires:	ruby

BuildRequires:	rubygems-devel
#BuildRequires:	rubygem(rake)
#BuildRequires:	rubygem(minitest)
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(test-unit-rr)
Requires:	ruby(rubygems)
Provides:	rubygem(%{gem_name}) = %{version}-%{release}
Conflicts:	rubygem-gettext < 2.0.0
%if 0%{?ruby19} < 1
Obsoletes:	ruby-%{gem_name} = %{version}-%{release}
Provides:	ruby-%{gem_name} = %{version}-%{release}
%endif

%description
Ruby-Locale is the pure ruby library which provides basic and general purpose
APIs for localization.
It aims to support all environments which ruby works and all kind of programs
(GUI, WWW, library, etc), and becomes the hub of other i18n/l10n libs/apps to 
handle major locale ID standards. 

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
Provides:	ruby(%{gem_name}) = %{version}-%{release}

%description	-n ruby-%{gem_name}
This package provides non-Gem support for %{gem_name}.

%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

%if 0%{?usegit} >= 1
tar xf %{SOURCE0}
cd %{gem_name}
find . -print0 | xargs -0 chmod go+rX

# Fixup version
sed -i -e 's|VERSION = "[0-9\.][0-9\.]*"|VERSION = "%{version}"|' \
	lib/locale/version.rb
%else
gem unpack %{SOURCE0}
cd %{gem_name}-%{version}
gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
%endif

gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# The following method is completely copied from rubygem-gettext
# spec file
#
# Create symlinks

create_symlink_rec(){

ORIGBASEDIR=$1
TARGETBASEDIR=$2

## First calculate relative path of ORIGBASEDIR 
## from TARGETBASEDIR
TMPDIR=$TARGETBASEDIR
BACKDIR=
DOWNDIR=
num=0
nnum=0
while true
do
	num=$((num+1))
	TMPDIR=$(echo $TMPDIR | sed -e 's|/[^/][^/]*$||')
	DOWNDIR=$(echo $ORIGBASEDIR | sed -e "s|^$TMPDIR||")
	if [ x$DOWNDIR != x$ORIGBASEDIR ]
	then
		nnum=0
		while [ $nnum -lt $num ]
		do
			BACKDIR="../$BACKDIR"
			nnum=$((nnum+1))
		done
		break
	fi
done

RELBASEDIR=$( echo $BACKDIR/$DOWNDIR | sed -e 's|//*|/|g' )

## Next actually create symlink
pushd %{buildroot}/$ORIGBASEDIR
find . -type f | while read f
do
	DIRNAME=$(dirname $f)
	BACK2DIR=$(echo $DIRNAME | sed -e 's|/[^/][^/]*|/..|g')
	mkdir -p %{buildroot}${TARGETBASEDIR}/$DIRNAME
	LNNAME=$(echo $BACK2DIR/$RELBASEDIR/$f | \
		sed -e 's|^\./||' | sed -e 's|//|/|g' | \
		sed -e 's|/\./|/|' )
	ln -s -f $LNNAME %{buildroot}${TARGETBASEDIR}/$f
done
popd

}

%if 0%{?ruby19} < 1
create_symlink_rec %{gem_instdir}/lib %{ruby_sitelib}
%endif

# Clean up unneeded files
rm -f %{buildroot}%{gem_instdir}/.yardopts

%check
pushd .%{gem_instdir}
#rake test
# test/test_detect_cgi.rb needs test-unit-rr
ruby -Ilib:test:. -e 'require "test-unit" ; require "test/unit/rr" ; Dir.glob("test/test_*.rb").each {|f| require f}'
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{gem_instdir}/
%doc %{gem_instdir}/[A-Z]*
%doc %{gem_instdir}/doc/
%exclude %{gem_instdir}/Rakefile
%{gem_instdir}/lib/
#%%{gem_instdir}/*.rb

%{gem_cache}
%{gem_spec}

%files doc
%defattr(-,root,root,-)
%{gem_docdir}/
%{gem_instdir}/samples/
%{gem_instdir}/test/
%{gem_instdir}/*.gemspec

%if 0%{?ruby19} < 1
%files -n ruby-%{gem_name}
%defattr(-,root,root,-)
%{ruby_sitelib}/%{gem_name}.rb
%{ruby_sitelib}/%{gem_name}/
%endif

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.1.2-1.2
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.1.2-1.1
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.2-1
- 2.1.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.1-1
- 2.1.1
- Use Ruby as BR, ruby(release) pulls in jruby

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 24 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.0-1
- 2.1.0

* Mon Oct 14 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.9-4.D20131012gitbc30e1b7f8
- Use upstream git head to fix test failure on ARM

* Fri Oct 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.9-3
- Do test suite in cleaner way

* Thu Sep 26 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.9-1
- 2.0.9

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.8-3
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 11 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.0.8-1
- 2.0.8

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.5-5
- Fix conditionals for F17 to work for RHEL 7 as well.

* Sun Jan 29 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.0.5-4
- F-17: rebuild against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 12 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- gems.rubyforge.org gem file seems old, changing Source0 URL for now

* Wed Nov 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.5-1
- 2.0.5
- Fix the license tag

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-2
- F-12: Mass rebuild

* Wed May 27 2009  Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-1
- 2.0.4

* Mon May 11 2009  Mamoru Tasaka <mtasaka@ios.s.u-tokyo.ac.jp> - 2.0.3-1
- 2.0.3

* Tue Apr 21 2009  Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-1
- 2.0.1

* Thu Mar 26 2009  Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-1
- Initial package
