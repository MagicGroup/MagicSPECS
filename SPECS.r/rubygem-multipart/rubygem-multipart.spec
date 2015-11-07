# Generated from multipart-0.2.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name multipart

Summary: Add multipart (file upload) support to Net::HTTP::Post
Name: rubygem-%{gem_name}
Version: 0.2.1
Release: 12%{?dist}
Group: Development/Languages
License: Public Domain
URL: http://rubyforge.org/projects/multipart
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone git://rubyforge.org/multipart.git && cd multipart
# tar czvf multipart-tests.tgz tests/
Source1: %{gem_name}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.8.3
BuildRequires: rubygem(test-unit)
BuildArch: noarch

%description
Multipart is a gem that adds support to multipart/form-encoded and
multipart/mixed (file upload) to Net::HTTP::Post.  Nothing more, nothing less.
Currently it supports a file param with multiple files, but not multiple file
params.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}

ruby tests/test.rb
popd


%files
%{gem_instdir}/multipart.rb
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.2.1-12
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.2.1-11
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 16 2014 Vít Ondruch <vondruch@redhat.com> - 0.2.1-9
- Fix FTBFS in Rawhide (rhbz#1107170).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 0.2.1-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.2.1-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Vít Ondruch <vondruch@redhat.com> - 0.2.1-1
- Initial package
