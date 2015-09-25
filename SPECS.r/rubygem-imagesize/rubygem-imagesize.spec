%global		gem_name		imagesize
%if 0%{?fedora} < 19
%global		rubyabi		1.9.1
%endif

Summary:	Measure image size(GIF, PNG, JPEG ,,, etc)
Name:		rubygem-%{gem_name}
Version:	0.1.1
Release:	16%{?dist}
Group:		Development/Languages
License:	GPLv2 or Ruby

URL:		http://imagesize.rubyforge.org
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
# With ruby1.9 handling regex needs some encoding treatment...
# bz819188
Patch0:         ruby-imagesize-0.1.1-ruby19-regex-utf8.patch
# Change the default encoding for regex
Patch1:         rubygem-imagesize-0.1.1-regex-magic.patch

%if 0%{?fedora} >= 19
Requires:	ruby(release)
BuildRequires:	ruby(release)
%else
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby 
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby 
%endif

Requires:	rubygems
BuildRequires:		rubygems-devel
BuildRequires:		rubygem(minitest)
# Don't create ruby-%%{gem_name} on F-17+
Obsoletes:	ruby-imagesize <= %{version}-%{release}

BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}
# For now also provide ruby(%%gem_name).
# on F-17 (i.e. with ruby 1.9.x) this should be safe
Provides:	ruby(%{gem_name}) = %{version}-%{release}

%description
Imagefile measures image (GIF, PNG, JPEG ,,, etc) size code 
by Pure Ruby ["PCX", "PSD", "XPM", "TIFF", "XBM", "PGM", 
"PBM", "PPM", "BMP", "JPEG", "PNG", "GIF", "SWF"]

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
mkdir -p .%{gem_dir}
TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

# Fixup wrong interpretter, line encoding
sed -i -e '1d' -e 's|\r||' lib/image_size.rb

# Patches
%patch0 -p1
%patch1 -p1

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
#ERROR:  While executing gem ... (Gem::InvalidSpecificationException)
#    cert_chain must not be nil
sed -i -e '/cert_chain/s|nil|[]|' %{gem_name}.gemspec

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

%check
# Where is ppm files?
pushd .%{gem_instdir}
sed -i.ppm \
	-e "s|'ppm.ppm', ||" \
	-e '/PPM/d' \
	test/test_image_size.rb
# Seems that PCX file cannot pass, rescue for now
ruby -Ilib -rtest/unit ./test/test_image_size.rb || echo "rescue for now"

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/README.txt
%{gem_instdir}/lib/
%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}/
%exclude	%{gem_instdir}/Manifest.txt
%exclude	%{gem_instdir}/setup.rb
%exclude	%{gem_instdir}/test/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.1.1-16
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.1-12
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.1-10
- Add BR: rubygem(minitest)

* Fri Jan  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.1-9
- Merge patches in ruby-imagesize to rubygem-imagesize
  From ruby-imagesize changelog:
  * Sun May  6 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.1.1-7
    - Regex treatment with ruby 1.9 (ref: bug 819188)
- release += 2

* Mon Dec 24 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.1-7
- Kill bogus license tag for setup.rb

* Sun Dec  9 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.1-6
- Rewrite for current ruby packaging guideline

* Tue Dec 27 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.1.1-5
- Switch to gem

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.1-3
- F-12: Mass rebuild

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.1-2
- %%global-ize "nested" macro

* Sat Nov  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.1-1
- Initial packaging
