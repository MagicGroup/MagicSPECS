# Generated from rubyforge-0.4.4.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname rubyforge
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global	 rubyabi 1.8

# Depency loop here. Kill test when resolving dependency loop
# is needed
%global enable_test 1

%if %{?fedora:0%{fedora} >= 17}%{?rhel:0%{rhel} >= 7}
%global	gem_name	%{gemname}
%global	gemdir	%{gem_dir}
%global	geminstdir	%{gem_instdir}
%if 0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif
%global	ruby19	1
%else
%global	ruby19	0
%endif

Summary:       A script which automates a limited set of rubyforge operations
Name:          rubygem-%{gemname}
Version:       2.0.4
Release:       14%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://rubyforge.org/projects/codeforpeople
Source0:       http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if 0%{?fedora} >= 19
Requires:	ruby(release)
BuildRequires:	ruby(release)
%else
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby 
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby 
%endif

Requires:      rubygems
Requires:      rubygem(json) >= 1.1.7
BuildRequires: rubygems
%if %{enable_test}
# For %%check
#BuildRequires: rubygem(rake)
BuildRequires: rubygem(json)
BuildRequires: rubygem(minitest)
# The following line causes dependency loop
BuildRequires: rubygem(hoe)
%endif
%if 0%{?ruby19} > 0
BuildRequires: rubygems-devel
%endif
BuildArch:     noarch
Provides:      rubygem(%{gemname}) = %{version}

%description
A script which automates a limited set of rubyforge operations.

%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

mkdir -p ./%{gemdir}
%gem_install -n %{SOURCE0}

# json_pure -> json
find . -name Rakefile -or -name \*.gemspec | \
	xargs sed -i -e 's|json_pure|json|g'

%if 0%{?fedora} >= 21
find . -name test_*.rb | \
	xargs sed -i \
		-e 's|test/unit|minitest/autorun|' \
		-e 's|Test::Unit::TestCase|Minitest::Test|' \
		-e 's|assert_raise |assert_raises |'
%endif

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{_prefix}/* %{buildroot}/%{_prefix}/


find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x
chmod 0755 %{buildroot}%{geminstdir}/lib/rubyforge.rb
chmod 0755 %{buildroot}%{geminstdir}/bin/rubyforge
chmod 0755 %{buildroot}%{_bindir}/rubyforge

%check
%if ! %{enable_test}
exit 0
%endif

mkdir TMP
export TMPDIR=$(pwd)/TMP

pushd .%{geminstdir}
ruby -Ilib:bin:test:. \
	-e 'Dir.glob("test/test_*.rb").each {|f| require f}'
popd

%files
%defattr(-, root, root, -)
%{_bindir}/rubyforge
%dir %{geminstdir}
%{geminstdir}/lib/
%{geminstdir}/bin/
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%doc %{geminstdir}/History.txt
%doc %{geminstdir}/Manifest.txt
%doc %{geminstdir}/README.txt

%files doc
%defattr(-,root,root,-)
%{gemdir}/doc/%{gemname}-%{version}
%{geminstdir}/Rakefile
%{geminstdir}/test/


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 26 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.4-13
- Use minitest directly, instead of rake
- Adjust for minitest 5

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar  5 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.4-10
- Enable test suite again

* Thu Mar  5 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.4-9
- F-19: Rebuild for ruby 2.0.0, once kill test suite for bootstrap

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.4-6
- Fix conditionals for F17 to work for RHEL 7 as well.

* Tue Jan 24 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.0.4-5
- F-17: rebuild against ruby 19

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-3
- F-15 mass rebuild

* Thu Sep 16 2010 Mamotu Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-2
- Split out document files

* Thu Mar  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-1
- Update to 2.0.4
- Replace json_pure to json (bug 570252)

* Mon Feb 15 2010 Darryl L. Pierce <dpierce@redhat.com> - 2.0.3-1
- Added new dependency on rubygem-json >= 1.1.7.
- Release 2.0.3 of RubyForge.

* Tue Sep 15 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.0.5-1
- Release 1.0.5 of RubyForge.

* Sat Aug  8 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.0.4-1
- Release 1.0.4 of RubyForge.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Darryl Pierce <dpierce@redhat.com> - 1.0.3-1
- Release 1.0.3 of RubyForge.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Darryl Pierce <dpierce@redhat.com> - 1.0.2-2
- Provided the wrong gem as source.

* Tue Jan 06 2009 Darryl Pierce <dpierce@redhat.com> - 1.0.2-1
- Release 1.0.2 of Rubyforge.

* Thu Oct 23 2008 Darryl Pierce <dpierce@redhat.com> - 1.0.1-1
- Release 1.0.1 of Rubyforge.

* Mon Jun 09 2008 Darryl Pierce <dpierce@redhat.com> - 1.0.0-1
- New version of RubyForge released.

* Wed May 14 2008 Darryl Pierce <dpierce@redhat.com> - 0.4.5-2
- Figured out how to do a proper build.

* Mon May 12 2008 Darryl Pierce <dpierce@redhat.com> - 0.4.5-1
- New version of the gem released.

* Tue Apr 29 2008 Darryl Pierce <dpierce@redhat.com> - 0.4.4-3
- Fixed the executable attribute for rubyforge.rb.

* Mon Apr 28 2008 Darryl Pierce <dpierce@redhat.com> - 0.4.4-2
- Updated the spec to comply with Ruby packaging guidelines.

* Fri Apr 18 2008 Darryl Pierce <dpierce@redhat.com> - 0.4.4-1
- Initial package
