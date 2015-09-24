# Generated from jquery-rails-2.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name jquery-rails

Name: rubygem-%{gem_name}
Version: 4.0.4
Release: 1%{?dist}
Summary: Use jQuery with Rails 4+
Group: Development/Languages
License: MIT
URL: http://rubygems.org/gems/jquery-rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: js-jquery1
Requires: js-jquery
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: web-assets-devel
# Unfortunately, lib/jquery/rails/version.rb specifies exact versions of
# bundled jquery, so be specific with the require to keep this relieable.
BuildRequires: js-jquery1 = 1.11.2
BuildRequires: js-jquery = 2.1.3
BuildArch: noarch

%description
This gem provides jQuery and the jQuery-ujs driver for your Rails 4+
application.


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

# Remove vendored jQuery but keep jquery-ujs.
rm .%{gem_instdir}/vendor/assets/javascripts/jquery{,2}.*

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

for file in %{_jsdir}/jquery/1/*; do
  ln -s -f $file -t %{buildroot}%{gem_instdir}/vendor/assets/javascripts/
done

for file in %{_jsdir}/jquery/2/*; do
  ln -s -f $file %{buildroot}%{gem_instdir}/vendor/assets/javascripts/$(basename $file | sed 's/jquery/jquery2/')
done

%check
pushd .%{gem_instdir}
# no tests :( but they are comming back again shortly!
# see https://github.com/rails/jquery-rails/pull/56
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
# bunch of bundled JS files here
%{gem_instdir}/vendor
%exclude %{gem_cache}
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/Gemfile.lock
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/VERSIONS.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/jquery-rails.gemspec

%changelog
* Fri Jun 19 2015 Vít Ondruch <vondruch@redhat.com> - 4.0.4-1
- Update to jquery-rails 4.0.4.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Josef Stribny <jstribny@redhat.com> - 3.1.0-1
- Update to jquery-rails 3.1.0

* Thu Feb 06 2014 Josef Stribny <jstribny@redhat.com> - 3.0.4-2
- Fix license to MIT only

* Wed Oct 23 2013 Josef Stribny <jstribny@redhat.com> - 3.0.4-1
- Update to jquery-rails 3.0.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.2-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.2-1
- Initial package
