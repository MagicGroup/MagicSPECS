# Generated from httparty-0.6.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name httparty

Summary: Makes HTTP fun! Also, makes consuming restful web services dead easy
Name: rubygem-%{gem_name}
Version: 0.13.1
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://jnunemaker.github.com/httparty
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://github.com/jnunemaker/httparty/pull/192
Patch0: rubygem-httparty-0.13.1-make-tests-run-with-rspec-2.10.patch
Patch1: rubygem-httparty-0.13.1-fix-its-for-rpsec-2.patch
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(fakeweb)
BuildRequires: rubygem(multi_xml)
BuildArch: noarch

%description
Makes HTTP fun! Also, makes consuming restful web services dead easy.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
%patch1 -p1
popd

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{_bindir} -type f | xargs chmod a+x

# Fix permissions.
chmod a+x %{buildroot}%{gem_instdir}/script/release

%check
pushd .%{gem_instdir}
LANG=en_US.utf8 rspec spec
popd

%files
%exclude %{gem_instdir}/.travis.yml
%{_bindir}/httparty
%dir %{gem_instdir}
%{gem_instdir}/bin
%exclude %{gem_instdir}/.*
%{gem_libdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/History
%{gem_cache}
%{gem_spec}

%files doc
%{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/Guardfile
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/httparty.gemspec
%{gem_instdir}/script
%{gem_instdir}/spec
%{gem_instdir}/website
%{gem_instdir}/features
%{gem_instdir}/*.yml

%changelog
* Thu Jul 10 2014 Vít Ondruch <vondruch@redhat.com> - 0.13.1-1
- Update to httparty 0.13.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.10.2-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Updated to Httparty 0.10.2.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 07 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.1-1
- Rebuilt for Ruby 1.9.3
- Update to version 0.8.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 01 2011 <stahnma@fedoraproject.org> - 0.7.4-1
- New version upstream

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 07 2010 Michael Stahnke <stahnma@fedorapojrect.org> - 0.6.1-2
- Review updates
- Changed to strict version of rubygem(crack) for Requires

* Sat Aug 07 2010 Michael Stahnke <stahnma@fedoraproject.org> - 0.6.1-1
- Initial package
