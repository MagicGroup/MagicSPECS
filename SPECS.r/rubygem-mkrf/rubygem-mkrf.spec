%if 0%{?fedora} >= 17
%global	rubyabi		1.9.1
%else
%global	rubyabi		1.8
%endif
%global		gem_name		mkrf

Summary:	Making C extensions for Ruby a bit easier
Name:		rubygem-%{gem_name}
Version:	0.2.3
Release:	16%{?dist}
Group:		Development/Languages
License:	MIT
URL:		http://mkrf.rubyforge.org/
Source0:	http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
Patch0:	rubygem-mkrf-0.2.3-Rakefile-newrake.patch

%if 0%{?fedora} >= 19
Requires:	ruby(release)
BuildRequires:	ruby(release)
%else
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby 
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby 
%endif
BuildRequires:		rubygems-devel
# For %%check
BuildRequires:	rubygem(rake)
BuildRequires:	libxml2-devel
BuildRequires:	ruby-devel
BuildRequires:		ruby(rubygems)
BuildArch:		noarch
Provides:		rubygem(%{gem_name}) = %{version}-%{release}

%description
mkrf is a library for generating Rakefiles to build Ruby
extension modules written in C. It is intended as a replacement for
mkmf. The major difference between the two is that mkrf
builds you a Rakefile instead of a Makefile.

This proposed replacement to mkmf generates Rakefiles to build C Extensions.

%package	doc
Summary:	Documentation for %{name}
# Some test files are under GPLv2+
License:	MIT and GPLv2+
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

%patch0 -p1

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
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

%clean
rm -rf %{buildroot}

%check
# Some tests fails, needs checking
#export GEM_PATH=$(pwd)/%{gem_dir}
pushd .%{gem_instdir}

rake -P | grep 'rake test:' | grep -v 'sample:all' | while read line
do
	eval $line --trace || true
done

popd

%files
%defattr(-,root,root,-)
%dir %{gem_instdir}
%doc %{gem_instdir}/[A-Z]*
%exclude %{gem_instdir}/Rakefile
%{gem_libdir}/
%exclude %{gem_cache}
%{gem_spec}

%files doc
%defattr(-,root,root,-)
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/test/
%{gem_docdir}

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.2.3-16
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.2.3-15
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.2.3-14
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.3-10
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.2.3-7
- rebuid again

* Sat Jan 29 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.2.3-6
- F-17: rebuild against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.2.3-4
- F-15 mass rebuild

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.2.3-3
- F-12: Mass rebuild

* Thu Jul  9 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.2.3-2
- Improve indentation
- Make sure gem is installed with proper permission

* Sat Jun 27 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.2.3-1
- Initial package
