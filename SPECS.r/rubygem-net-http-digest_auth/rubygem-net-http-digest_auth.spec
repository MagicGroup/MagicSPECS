%global	gem_name	net-http-digest_auth
%if		0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif

Summary:	Implementation of RFC 2617 - Digest Access Authentication
Name:		rubygem-%{gem_name}
Version:	1.4
Release:	5%{?dist}

Group:		Development/Languages
# README.txt
License:	MIT
URL:		http://docs.seattlerb.org/net-http-digest_auth
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
BuildRequires:	rubygems-devel 
# %%check
BuildRequires:	rubygem(minitest)
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
An implementation of RFC 2617 - Digest Access Authentication.  At this time
the gem does not drop in to Net::HTTP and can be used for with other HTTP
clients.
In order to use net-http-digest_auth you'll need to perform some request
wrangling on your own.  See the class documentation at Net::HTTP::DigestAuth
for an example.


%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

# For minitest 4.7.0 (latest is 5.0.x)
sed -i -e 's|MiniTest::Test|MiniTest::Unit::TestCase|' \
	test/test_net_http_digest_auth.rb

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
mkdir -p .%{gem_dir}
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# Clean up
rm -f %{buildroot}%{gem_instdir}/{.autotest,.gemtest}

%check
pushd .%{gem_instdir}
ruby -Ilib test/test_net_http_digest_auth.rb
popd

%files
%dir	%{gem_instdir}/
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile

%{gem_libdir}/
%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}/
%doc	%{gem_instdir}/sample/
%exclude	%{gem_instdir}/test/

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.4-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.4-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4-1
- 1.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3-1
- 1.3

* Tue Feb 26 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.2-2
- Support newer ruby packaging guideline

* Mon Jan 07 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.1-1
- Initial package
