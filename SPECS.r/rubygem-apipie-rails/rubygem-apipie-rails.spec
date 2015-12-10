# Generated from apipie-rails-0.0.13.gem by gem2rpm -*- rpm-spec -*-
%global gem_name apipie-rails

Name: rubygem-%{gem_name}
Version: 0.3.4
Release: 4%{?dist}
Summary: Rails REST API documentation tool
Group: Development/Languages
# The project itself is MIT
# For ASL 2.0, see https://github.com/Pajk/apipie-rails/issues/66
# (bundled JS files under app/public)
License: MIT and ASL 2.0
URL: http://github.com/Pajk/apipie-rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Migrate the test suite to RSpec 3.x.
# https://github.com/Apipie/apipie-rails/pull/382
Patch0: rubygem-apipie-rails-0.3.4-RSpec3-support.patch
# TODO: https://lists.fedoraproject.org/pipermail/packaging/2015-July/010794.html
Requires: js-jquery1
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: js-jquery1
BuildRequires: rubygem(rails)
BuildRequires: rubygem(rspec-rails)
BuildRequires: rubygem(sqlite3)
BuildRequires: web-assets-devel
BuildArch: noarch

%description
Apipie-rails is a DSL and Rails engine for documenting your RESTful API.
Instead of traditional use of #comments, Apipie lets you describe the code,
through the code. This brings advantages like:

* No need to learn yet another syntax, you already know Ruby, right?
* Possibility of reusing the docs for other purposes (such as validation)
* Easier to extend and maintain (no string parsing involved)
* Possibility of reusing other sources for documentation purposes (such as
  routes etc.)

The documentation is available from within your app (by default under the
/apipie path.) In development mode, you can see the changes as you go. It's
markup language agnostic, and even provides an API for reusing the
documentation data in JSON.


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

pushd .%{gem_instdir}
%patch0 -p1

# Replace bundled jQuery by link to system version.
# https://github.com/Apipie/apipie-rails/pull/386
ln -sf %{_jsdir}/jquery/1/jquery.js app/public/apipie/javascripts/bundled/jquery-1.7.2.js
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Remove empty .gitkeep files, that rpmlint complains about, we don't need
# them in RPMs.
find %{buildroot}%{gem_instdir}/spec -type f -name '.gitkeep' -exec rm {} \;

%check
pushd .%{gem_instdir}
# we don't want to use Bundler for build
rm Gemfile*
sed -i "/require 'bundler\/setup'/ s/^/#/" spec/spec_helper.rb
sed -i "/Bundler.require/ s/^/#/" spec/dummy/config/application.rb

rspec spec
popd


%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/APACHE-LICENSE-2.0
%license %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/app
%{gem_instdir}/config
%{gem_libdir}
# exclude useless rel-eng directory
%exclude %{gem_instdir}/rel-eng
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile*
%doc %{gem_instdir}/README.rst
%doc %{gem_instdir}/NOTICE
%{gem_instdir}/Rakefile
%{gem_instdir}/apipie-rails.gemspec
%{gem_instdir}/spec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.3.4-4
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.3.4-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3.4-2
- 为 Magic 3.0 重建

* Wed Jul 01 2015 Vít Ondruch <vondruch@redhat.com> - 0.3.4-1
- Update to apipie-rails 0.3.4.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 26 2013 Vít Ondruch <vondruch@redhat.com> - 0.0.22-1
- Update to apipie-rails 0.0.22.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Vít Ondruch <vondruch@redhat.com> - 0.0.21-1
- Update to apipie-rails 0.0.21.

* Thu Mar 28 2013 Vít Ondruch <vondruch@redhat.com> - 0.0.13-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.13-2
- Fixed some file permission issues.
- Keep the specs in -doc subpackage.
- Run the tests without git.
- Add runtime dependency on rubygem(rails).

* Tue Nov 20 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.13-1
- Initial package
