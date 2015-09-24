# Generated from font-awesome-rails-4.1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name font-awesome-rails

Name: rubygem-%{gem_name}
Version: 4.4.0.0
Release: 1%{?dist}
Summary: An asset gemification of the font-awesome icon font library
Group: Development/Languages
# Fonts are licensed with SIL Open Font License 1.1
License: MIT and OFL
URL: https://github.com/bokmann/font-awesome-rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: fontawesome-fonts >= 4.4.0
Requires: fontawesome-fonts < 4.5.0
BuildRequires: rubygems-devel
BuildRequires: rubygem(railties)
BuildRequires: rubygem(sass-rails)
BuildRequires: fontpackages-devel
BuildRequires: fontawesome-fonts
BuildArch: noarch

%description
A font-awesome icon font library for the Rails asset pipeline.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Symlink *.otf and *.ttf as this is shipped in fontawesome-fonts pkg
rm %{buildroot}%{gem_instdir}/app/assets/fonts/FontAwesome.otf
ln -s %{_fontbasedir}/fontawesome/FontAwesome.otf %{buildroot}%{gem_instdir}/app/assets/fonts/FontAwesome.otf
rm %{buildroot}%{gem_instdir}/app/assets/fonts/fontawesome-webfont.ttf
ln -s %{_fontbasedir}/fontawesome/fontawesome-webfont.ttf %{buildroot}%{gem_instdir}/app/assets/fonts/fontawesome-webfont.ttf

# Fix permissions
find %{buildroot}%{gem_dir}/**/* -type f | xargs chmod 0644

# Remove shebang from non-executable Rakefile
sed -i -e '1d' %{buildroot}%{gem_instdir}/Rakefile

%check
pushd .%{gem_instdir}
# Get rid of bundler
sed -i -e '6d' test/dummy/config/application.rb
ruby -Ilib:test:app:app/helpers/font_awesome/rails -rrails -raction_view -rsass -rsass-rails -rfont-awesome-rails -ricon_helper \
     -e 'Dir.glob "./test/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{gem_instdir}/app
%license %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Mon Sep 21 2015 Josef Stribny <jstribny@redhat.com> - 4.4.0.0-1
- Update to 4.4.0.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Nov 12 2014 Josef Stribny <jstribny@redhat.com> - 4.1.0.0-4
- Fix version dependency on font-awesome-fonts

* Mon Sep 22 2014 Josef Stribny <jstribny@redhat.com> - 4.1.0.0-3
- Remove shebang from Rakefile
- State exact version dependency on fontawesome-fonts

* Tue Sep 16 2014 Josef Stribny <jstribny@redhat.com> - 4.1.0.0-2
- Fix permissions

* Fri Jul 18 2014 Josef Stribny <jstribny@redhat.com> - 4.1.0.0-1
- Initial package
