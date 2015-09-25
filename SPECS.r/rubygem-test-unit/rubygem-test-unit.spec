%global	gem_name	test-unit

# svn repository
# http://test-unit.rubyforge.org/svn/trunk/

Summary:	Improved version of Test::Unit bundled in Ruby 1.8.x
Name:		rubygem-%{gem_name}
Version:	3.1.3
Release:	101%{?dist}
Group:		Development/Languages
# lib/test/unit/diff.rb is under GPLv2 or Ruby or Python
# lib/test-unit.rb is under LGPLv2+ or Ruby
# Other file: GPLv2 or Ruby
License:	(GPLv2 or Ruby) and (GPLv2 or Ruby or Python) and (LGPLv2+ or Ruby)
URL:		http://test-unit.github.io/

Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	ruby(release)
BuildRequires:	rubygems
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(power_assert)
# For %%check
#BuildRequires:	rubygem(rake)
#BuildRequires:	rubygem(hoe)
Requires:	ruby(release)
Requires:	rubygems

BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
Test::Unit 2.x - Improved version of Test::Unit bundled in
Ruby 1.8.x.
Ruby 1.9.x bundles minitest not Test::Unit. Test::Unit
bundled in Ruby 1.8.x had not been improved but unbundled
Test::Unit (Test::Unit 2.x) will be improved actively.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T
# Gem repack
TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

#find . -name \*.gem | xargs chmod 0644
find . -type f | xargs chmod ugo+r

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# Keep testrb2
%if 0%{?fedora} < 22
mkdir %{buildroot}%{_bindir}
cat %{_bindir}/testrb | \
	sed -e '\@require@s|test/unit|test-unit|' \
	> %{buildroot}%{_bindir}/testrb2
chmod 0755 %{buildroot}%{_bindir}/testrb2
%endif

%check
pushd .%{gem_instdir}
#rake test --trace
ruby -Ilib ./test/run-test.rb
popd

%files
%defattr(-,root,root,-)
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile

%if 0%{?fedora} < 22
%{_bindir}/testrb2
%endif
%{gem_instdir}/lib/

%exclude	%{gem_cache}
%{gem_spec}

%files	doc
%defattr(-,root,root,-)
%{gem_instdir}/doc/
# Keep below for this package
%{gem_instdir}/Rakefile
%{gem_instdir}/sample/
%{gem_instdir}/test/

%{gem_docdir}/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.1.3-101
- 为 Magic 3.0 重建

* Mon Jul 27 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.3-100
- 3.1.3

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-100
- 3.1.2

* Fri May 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.1-100
- 3.1.1

* Fri May 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.0-100
- 3.1.0

* Tue Jan 13 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.9-101
- Kill 2-year-old testrb2 support on F-22+

* Wed Dec 29 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.9-100
- 3.0.9

* Sun Dec 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.8-100
- Bump release massively (for ruby srpm)

* Sun Dec 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.8-1
- 3.0.8

* Thu Dec  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.7-1
- 3.0.7

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.5.5-1
- 2.5.5

* Thu Feb 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.5.4-3
- Patch for CSV support (patch by upstream)

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.5.4-2
- Rebuild for ruby 2.0.0

* Sun Feb  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.5.4-1
- 2.5.4

* Wed Jan  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.5.3-1
- 2.5.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.4.5-3
- Fix conditionals for F17 to work for RHEL 7 as well.

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.5-2
- 2.4.5

* Sun Jan 15 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.4-1
- 2.4.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-2
- F-17: Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.3-1
- 2.4.3

* Sun Nov 27 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.2-1
- 2.4.2

* Wed Nov 16 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.1-1
- 2.4.1

* Mon Sep 19 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.0-1
- 2.4.0

* Thu Aug 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.2-1
- 2.3.2

* Sun Aug 14 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.1-1
- 2.3.1

* Sun Apr 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.0-1
- 2.3.0

* Fri Feb 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.2.0-1
- 2.2.0

* Mon Feb 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.2-2
- F-15 mass rebuild

* Thu Nov 26 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.2-1
- 2.1.2

* Sun Sep 19 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.1-2
- Fix up license tag

* Sat Sep 18 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.1-1
- Initial package
