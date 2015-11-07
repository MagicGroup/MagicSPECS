%global gem_name gettext_i18n_rails

Name: rubygem-%{gem_name}
Version: 1.2.3
Release: 3%{?dist}
Summary: Simple FastGettext Rails integration
Group: Development/Languages
License: MIT
URL: http://github.com/grosser/gettext_i18n_rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/grosser/gettext_i18n_rails.git && cd gettext_i18n_rails && git checkout v1.2.3
# tar czvf gettext_i18n_rails-1.2.3-specs.tgz spec
Source1: %{gem_name}-%{version}-specs.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(actionmailer)
BuildRequires: rubygem(activerecord)
BuildRequires: rubygem(fast_gettext)
BuildRequires: rubygem(gettext)
BuildRequires: rubygem(haml)
BuildRequires: rubygem(railties)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(ruby_parser)
BuildRequires: rubygem(slim)
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(temple)
BuildArch: noarch

%description
Translate via FastGettext, use any other I18n backend as extension/fallback.


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
tar xzf %{SOURCE1}

rspec spec
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.2.3-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.3-2
- 为 Magic 3.0 重建

* Thu Jun 25 2015 Vít Ondruch <vondruch@redhat.com> - 1.2.3-1
- Update to gettext_i18n_rails 1.2.3.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 20 2014 Vít Ondruch <vondruch@redhat.com> - 1.0.5-1
- Update to gettext_i18n_rails 1.0.5.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 20 2013 Vít Ondruch <vondruch@redhat.com> - 0.10.1-1
- Update to gettext_i18n_rails 0.10.1.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 17 2013 Josef Stribny <jstribny@redhat.com> - 0.9.4-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Updated to version 0.9.4.

* Mon Feb 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.2-1
- Updated to version 0.9.2.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 5 2012 Josef Stribny <jstribny@redhat.com> - 0.7.0-1
- Update to version 0.7.1

* Fri Jul 27 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.6-1
- Updated to version 0.6.6.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.0-2
- Rebuilt for Ruby 1.9.3.

* Wed Jan 04 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.0-1
- New version.
- Modified Requires and BuildRequires according to new version.

* Mon Jan 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.6-1
- Update to the latest version.
- Changed license to Public Domain only.
- Moved init.rb to doc subpackage, as it is not needed for runtime.
- Fixed dependencies according to the gemspec in this version.

* Wed Oct 26 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.0-1
- Upgraded to the latest version.
- Removed the patch that fixed failing tests (fixed in new version).
- Clarified the license.
- Moved Readme.md to the main package, as it contains licensing information.
- Moved VERSION to the main package and unmarked it as a doc, as it's needed for runtime.

* Wed Sep 14 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.20-1
- Initial package
