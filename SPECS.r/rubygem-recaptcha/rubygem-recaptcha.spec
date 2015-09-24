%global gem_name recaptcha

Name: rubygem-%{gem_name}
Version: 0.4.0
Release: 1%{?dist}
Summary: Helpers for the reCAPTCHA API
Group: Development/Languages
License: MIT
URL: http://github.com/ambethia/recaptcha
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
This plug-in adds helpers for the reCAPTCHA API.
In your views you can use the recaptcha_tags method
to embed the needed JavaScript, and you can validate
in your controllers with verify_recaptcha.

Beforehand you need to configure Recaptcha with your
custom private and public key. You may find detailed
examples below.
Exceptions will be raised if you call these methods
and the keys can’t be found.


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


%check
pushd .%{gem_instdir}
ruby -Ilib -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}


%files doc
%{gem_docdir}
%doc %{gem_instdir}/CHANGELOG
%{gem_instdir}/Gemfile*
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/init.rb
%{gem_instdir}/test

%changelog
* Fri Jun 26 2015 Vít Ondruch <vondruch@redhat.com> - 0.4.0-1
- Update to reCAPTCHA 0.4.0.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Josef Stribny <jstribny@redhat.com> - 0.3.5-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Fri Mar 15 2013 Akira TAGOH <tagoh@redhat.com> - 0.3.5-1
- New upstream release.
- spec file clean up.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 0.3.1-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 19 2011 Akira TAGOH <tagoh@localhost> - 0.3.1-1
- Initial package
