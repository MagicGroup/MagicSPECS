%global	gem_name	net-http-persistent

Summary:	Persistent connections using Net::HTTP plus a speed fix
Name:		rubygem-%{gem_name}
Version:	2.9.4
Release:	5%{?dist}
Group:		Development/Languages
License:	MIT

URL:		http://seattlerb.rubyforge.org/net-http-persistent
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0:		rubygem-net-http-persistent-2.1-no-net-test.patch

Requires:	ruby(release)
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(minitest)

Requires:	rubygems
BuildArch:	noarch

Provides:	rubygem(%{gem_name}) = %{version}

%description
Persistent connections using Net::HTTP plus a speed fix for 1.8.  It's
thread-safe too.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description    doc
This package contains documentation for %{name}.


%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

# For minitest 4.7.0 (latest is 5.0.x)
%if 0%{?fedora} < 21
sed -i -e 's|Mini[Tt]est::Test|MiniTest::Unit::TestCase|' \
	test/test_net_http_persistent*.rb
%endif

%patch0 -p1

# Don't use SSLv3
sed -i test/test_net_http_persistent_ssl_reuse.rb \
	-e 's|SSLv3|TLSv1_2|'

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

#chmod 0644 ./%{gem_dir}/cache/%{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}/%{gem_dir}/
rm -f %{buildroot}%{gem_instdir}/{.autotest,.gemtest}

%check
pushd .%{gem_instdir}
# testrb -Ilib test
ruby -Ilib:. -e 'Dir.glob("test/test_*.rb").each{|f| require f}'
popd

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile
%{gem_instdir}/lib/
%exclude	%{gem_cache}
%{gem_spec}

%files	doc
%exclude	%{gem_instdir}/Rakefile
%exclude	%{gem_instdir}/test/
%{gem_docdir}/

%changelog
* Tue Jun 30 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.4-5
- Don't use SSLv3 for test

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.4-3
- Use minitest 5 correctly for F-21+

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Feb 22 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.4-1
- 2.9.4

* Mon Feb 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.3-1
- 2.9.3

* Mon Jan 27 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.1-1
- 2.9.1

* Wed Aug  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9-1
- 2.9

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 21 2013 Vít Ondruch <vondruch@redhat.com> - 2.8-4
- Fix EL compatibility.
- Test are passing now.
- Cleanup.

* Thu Feb 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8-3
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8-1
- Update to 2.8

* Mon Nov 26 2012 Vít Ondruch <vondruch@redhat.com> - 2.1-6
- Add EL compatibility macros.
- Drop rubygem({hoe,rake}) build dependencies.

* Thu Aug  2 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.1-5
- Rescue test failure for now

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.1-3
- F-17: rebuild against ruby19

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  9 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.1-1
- 2.1

* Sun Aug 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.0-1
- 2.0

* Sun Aug 14 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8.1-1
- 1.8.1

* Mon Jul  4 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8-1
- 1.8

* Sun Apr 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.7-1
- 1.7

* Thu Mar 10 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.6.1-1
- 1.6.1

* Thu Mar  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.6-1
- 1.6

* Sat Feb 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.2-1
- 1.5.2
- Patch0 merged

* Sat Feb 12 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.1-1
- 1.5.1

* Thu Feb 10 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5-3
- Rescue the case where socket is Nil, for mechanize testsuite

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5-1
- 1.5

* Sun Jan 16 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.1-1
- Initial package
