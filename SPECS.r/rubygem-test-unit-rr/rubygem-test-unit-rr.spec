%global	gem_name	test-unit-rr
%if 0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif

Summary:	Test::Unit::RR - RR adapter for Test::Unit
Name:		rubygem-%{gem_name}
Version:	1.0.3
Release:	6%{?dist}
Group:		Development/Languages
# https://github.com/test-unit/test-unit-rr/issues/1
License:	LGPLv2+
URL:		http://rubyforge.org/projects/test-unit/
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem

%if 0%{?fedora} >= 19
Requires:	ruby(release)
BuildRequires:	ruby(release)
%else
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby 
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby 
%endif
Requires:	ruby(rubygems) 
Requires:	rubygem(test-unit)
Requires:	rubygem(rr)
BuildRequires:	rubygems-devel 
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(rr)
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
Test::Unit::RR - RR adapter for Test::Unit.


%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
# Gem repack
TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec

# Allow current test-unit version for now
sed -i \
	-e '/add_.*dependency.*test-unit/s|2.5.2|2.1.2|' \
	test-unit-rr.gemspec

# And for now change test-unit to test/unit
sed -i \
	-e '/require.*test-unit/s|^.*$|gem "test-unit"\nrequire "test/unit"|' \
	test/run-test.rb
sed -i \
	-e '/require/s|test-unit|test/unit|' \
	lib/test/unit/rr.rb 

gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

# Permission
find . -type f -print0 | xargs --null chmod go-w

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_instdir}/{Manifest.txt,Rakefile,*.gemspec}

%check
pushd .%{gem_instdir}
ruby -Ilib test/run-test.rb

%files
%dir	%{gem_instdir}
%{gem_libdir}/
%exclude	%{gem_cache}
%{gem_spec}

%doc	%{gem_instdir}/[A-Z]*
%doc	%{gem_instdir}/doc/

%files doc
%doc	%{gem_docdir}/
%exclude	%{gem_instdir}/test/

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.0.3-6
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.3-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.3-4
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 19 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.3-1
- 1.0.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.2-5
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.2-3
- Fix dependency for test-unit again

* Mon Dec 31 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.2-2
- Add BR: rubygem(test-unit), rubygem(rr)

* Sun Dec  9 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.2-1
- 1.0.2

* Sun Nov 04 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.1-1
- Initial package
