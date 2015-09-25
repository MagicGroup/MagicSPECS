# Generated from idn-0.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name		idn

Summary: Ruby Bindings for the GNU LibIDN library
Name: rubygem-%{gem_name}
Version: 0.0.2
Release: 16%{?dist}
Group: Development/Languages

# ASL license for ext/idn.c, ext/idn.h, ext/punycode.c and ext/stringprep.c
License: ASL 2.0 and LGPLv2+
URL: http://rubyforge.org/projects/idn/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0: rubygem-idn-0.0.2-Fix-for-ruby-1.9.x.patch
# Fixes failure due to change in default encoding in Ruby 2.0.
# http://rubyforge.org/tracker/index.php?func=detail&aid=29724&group_id=924&atid=3635
Patch1: rubygem-idn-0.0.2-ruby2-encoding-in-tests-fix.patch

BuildRequires: rubygems-devel
BuildRequires: libidn-devel
BuildRequires: ruby-devel
BuildRequires: rubygem(minitest)


%description
Ruby Bindings for the GNU LibIDN library, an implementation of the Stringprep, 
Punycode and IDNA specifications defined by the IETF Internationalized Domain 
Names (IDN) working group. 

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T
pushd ..
gem unpack %{SOURCE0}

pushd %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%patch0 -p0
%patch1 -p1

# Avoid "cert_chain must not be nil" error.
sed -i -e "10d" %{gem_name}.gemspec

gem build %{gem_name}.gemspec
popd
popd

%gem_install -n ../%{gem_name}-%{version}/%{gem_name}-%{version}.gem

%build

%install
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a ./* %{buildroot}/

cp -a .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo.
rm -rf %{buildroot}%{gem_instdir}/ext



## remove all shebang, set permission to 0644
find .%{gem_instdir}/{Rakefile,lib,spec} -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/bin\/env ruby/d'
find .%{gem_instdir}/{Rakefile,lib,spec} -type f | \
  xargs chmod 0644

%check
pushd .%{gem_instdir}

sed -i '/test\/unit/ s/^/#/' test/*.rb
ruby -rminitest/autorun -Itest:$(dirs +1)%{gem_extdir_mri} - << \EOF
  Test = Minitest
  Minitest::Test.send :alias_method, :assert_raise, :assert_raises;
  Dir.glob "./test/tc_*.rb", &method(:require)
EOF

popd

%files
%dir %{gem_instdir}/
%{gem_extdir_mri}
%exclude %{gem_libdir}
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/LICENSE
%{gem_spec}
%exclude %{gem_cache}

%files doc
%{gem_instdir}/Rakefile
%{gem_instdir}/NOTICE
%{gem_instdir}/README

%{gem_instdir}/test
%{gem_docdir}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.0.2-16
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Vít Ondruch <vondruch@redhat.com> - 0.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Josef Stribny <jstribny@redhat.com> - 0.0.2-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Shawn Starr <shawn.starr@rogers.com> - 0.0.2-6
- Use the proper way to do conversion within C ext code.

* Thu Feb 09 2012 Shawn Starr <shawn.starr@rogers.com> - 0.0.2-5
- Fix tests so it passes now

* Thu Feb 09 2012 Vít Ondruch <vondruch@redhat.com> - 0.0.2-4
- Rebuilt for Ruby 1.9.3.

* Sun Jan 29 2012 Shawn Starr <shawn.starr@rogers.com> - 0.0.2-3
- Fix build issue in mock, remove .yardoc since its not being
created anymore.

* Sun Nov 06 2011 Shawn Starr <shawn.starr@rogers.com> - 0.0.2-2
- Update spec based on bugzilla review feedback.

* Thu Jul 21 2011 Shawn Starr <shawn.starr@rogers.com> - 0.0.2-1
- Initial package
