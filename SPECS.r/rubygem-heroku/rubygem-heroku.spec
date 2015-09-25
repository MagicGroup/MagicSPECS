# Generated from heroku-2.0.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name heroku

Name: rubygem-%{gem_name}
Version: 3.41.3
Release: 2%{?dist}
Summary: Client library and CLI to deploy apps on Heroku
Group: Development/Languages
License: MIT
URL: http://heroku.com/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: %{_bindir}/git
BuildRequires: %{_bindir}/hostname
BuildRequires: %{_bindir}/openssl
BuildRequires: rubygem(excon)
BuildRequires: rubygem(fakefs)
BuildRequires: rubygem(heroku-api)
BuildRequires: rubygem(launchy)
BuildRequires: rubygem(net-ssh-gateway)
BuildRequires: rubygem(netrc)
BuildRequires: rubygem(rest-client)
BuildRequires: rubygem(rr)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(rubyzip)
BuildRequires: rubygem(webmock)
BuildArch: noarch
# There were attempts to remove OkJson:
# https://github.com/heroku/heroku/pull/887
# OkJson is allowed to be bundled:
# https://fedorahosted.org/fpc/ticket/113
Provides: bundled(okjson) = 20120328

%description
Client library and command-line tool to deploy and manage apps on Heroku.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Remove bundled root CA certificates.
rm %{buildroot}%{gem_instdir}/data/cacert.pem
rm -d %{buildroot}%{gem_instdir}/data

%check
pushd .%{gem_instdir}
# We don't care about coverage.
sed -i '/[Cc]overalls/ s/^/#/' spec/spec_helper.rb

# Git credentials has to be configured for several tests."
git config --global user.email "you@example.com"
git config --global user.name "Your Name"

# Heroku::Client rendezvous fixup hash:
# https://github.com/heroku/heroku/issues/1119
sed -i '/it "hash" do/a \      pending' spec/heroku/client/rendezvous_spec.rb

rspec spec
popd

%files
%license %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{_bindir}/heroku
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/README.md

%files doc
%doc %{gem_docdir}
%{gem_instdir}/spec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.41.3-2
- 为 Magic 3.0 重建

* Thu Aug 20 2015 Vít Ondruch <vondruch@redhat.com> - 3.41.3-1
- Update to heroku 3.41.3.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.30.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 30 2015 Vít Ondruch <vondruch@redhat.com> - 3.30.3-1
- Update to heroku 3.30.3.

* Mon May 26 2014 Vít Ondruch <vondruch@redhat.com> - 3.8.2-1
- Update to heroku 3.8.2.
- Drop root CA certificates.

* Fri May 17 2013 Josef Stribny <jstribny@redhat.com> - 2.39.3-1
- Update to heroku 2.39.3

* Tue Mar 12 2013 Vít Ondruch <vondruch@redhat.com> - 2.33.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Tue Mar 12 2013 Vít Ondruch <vondruch@redhat.com> - 2.33.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Vít Ondruch <vondruch@redhat.com> - 2.33.0-1
- Update to heroku 2.33.0.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Vít Ondruch <vondruch@redhat.com> - 2.24.0-2
- Fix dependencies.

* Fri Apr 06 2012 Vít Ondruch <vondruch@redhat.com> - 2.24.0-1
- Updated to heroku 2.24.0.

* Wed Apr 04 2012 Vít Ondruch <vondruch@redhat.com> - 2.23.0-1
- Updated to heroku 2.23.0.

* Tue Feb 14 2012 Vít Ondruch <vondruch@redhat.com> - 2.21.2-1
- Rebuilt for Ruby 1.9.3.
- Updated to heroku 2.21.2.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun May 01 2011  <Minnikhanov@gmail.com> - 2.0.4-1
- Updated heroku to latest upstream release (v.2.0.4 2011-04-28)

* Sat Apr 23 2011  <Minnikhanov@gmail.com> - 1.20.1-2
- Don't use "launchy" gem ver. >=0.4 (upstream run dependence limit)

* Sun Apr 10 2011  <Minnikhanov@gmail.com> - 1.20.1-1
- Updated heroku to latest upstream release (v.1.20.1 2011-04-07)

* Tue Feb 22 2011  <Minnikhanov@gmail.com> - 1.17.16-1
- Updated heroku to latest upstream release (v.1.17.16 2011-02-18)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 29 2011  <Minnikhanov@gmail.com> - 1.17.10-1
- Updated heroku to latest upstream release (v.1.17.10 2011-01-21)

* Thu Jan 13 2011  <Minnikhanov@gmail.com> - 1.17.5-1
- Updated heroku to latest upstream release

* Fri Jan 07 2011  <Minnikhanov@gmail.com> - 1.16.2-1
- Updated heroku to latest upstream release

* Fri Dec 24 2010  <Minnikhanov@gmail.com> - 1.15.1-1
- Updated heroku to latest upstream release

* Thu Dec 23 2010  <Minnikhanov@gmail.com> - 1.15.0-2
- Fix Comment 29 #661436 (Review Request)

* Tue Dec 21 2010  <Minnikhanov@gmail.com> - 1.15.0-1
- Updated heroku to latest upstream release

* Tue Dec 21 2010  <Minnikhanov@gmail.com> - 1.14.10-3
- Fix Comment 23 #661436 (Review Request)
- Remove '/.yardoc'.

* Sat Dec 18 2010  <Minnikhanov@gmail.com> - 1.14.10-2
- Fix Comment 18 #661436 (Review Request)
- Set Release: 2

* Fri Dec 17 2010  <Minnikhanov@gmail.com> - 1.14.10-1
- Fix Comment 13 #661436 (Review Request)

* Thu Dec 16 2010  <Minnikhanov@gmail.com> - 1.14.10-1
- Initial package

* Wed Dec 15 2010  <Minnikhanov@gmail.com> - 1.14.9-1
- Updated heroku to latest upstream release

* Mon Dec 13 2010  <Minnikhanov@gmail.com> - 1.14.8-1
- Fix Comment 4 #661436 (Review Request)

* Wed Dec 08 2010  <Minnikhanov@gmail.com> - 1.14.8-1
- Initial package

