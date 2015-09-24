%global	gem_name	clutter-gtk

Name:		rubygem-%{gem_name}
Version:	2.2.5
Release:	2%{?dist}
Summary:	Ruby binding of Clutter-GTK

License:	LGPLv2+
URL:		http://ruby-gnome2.sourceforge.jp/
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://raw.githubusercontent.com/ruby-gnome2/ruby-gnome2/master/COPYING.LIB
# renamed to avoid namespace collision on sourcedir
Source1:	COPYING.LIB.clutter-gtk

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(clutter)
BuildRequires:	rubygem(gtk3)
BuildRequires:	rubygem-glib2-devel
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(test-unit-notify)
BuildRequires:	%{_bindir}/xvfb-run
# See bug 904851 and below
BuildRequires:	mesa-dri-drivers
BuildRequires:	clutter-gtk

Requires:		clutter-gtk

BuildArch:	noarch

%description
Ruby/ClutterGTK is a Ruby binding of Clutter-GTK.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Adjust rubygems-gnome2 requirement to be more flexible
sed -i -e 's|= 2\.2\.5|>= 2.2.5|' %{gem_name}.gemspec

# Fix permission
find . -name \*.rb -print0 | xargs --null chmod 0644

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

install -cpm 644 %{SOURCE1} %{buildroot}%{gem_instdir}/COPYING.LIB

# cleanup
pushd %{buildroot}%{gem_instdir}
rm -rf \
	Rakefile \
	test/
popd

%check
pushd .%{gem_instdir}

mkdir tmp
touch \
	tmp/gobject-introspection-test-utils.rb \
	tmp/clutter-test-utils.rb

# Tweak test source directory
sed -i \
	-e '\@clutter_gtk_test_base =@s|clutter_gtk_base|File.dirname(__FILE__), ".."|' \
	test/run-test.rb

# Clutter-CRITICAL **:Unable to initialize Clutter: 
# Unable to find suitable fbconfig for the GLX context: 
# Failed to find any compatible fbconfigs
#
# So use screen depth 24, see bug 904851
#
# https://github.com/ruby-gnome2/ruby-gnome2/issues/274
# Umm.. under non-chroot environment, the following passes.
# However in mock environ the following sometimes fails.
# http://sources.gentoo.org/cgi-bin/viewvc.cgi/gentoo-x86/media-libs/clutter/clutter-1.18.4.ebuild?view=markup
# may suggest that this may be related to mesa driver issues,
# however I am not sure - disabled for now
#
test -n "$XAUTHORITY" || exit 0

xvfb-run -s "-screen 0 640x480x24" \
	ruby -Ilib:tmp:test ./test/run-test.rb

rm -rf tmp/
popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/COPYING.LIB

%{gem_libdir}
%{gem_spec}

%exclude	%{gem_cache}

%files doc
%doc	%{gem_docdir}
%doc	%{gem_instdir}/sample/

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.5-1
- 2.2.5

* Sun Dec 28 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.4-1
- 2.2.4

* Mon Dec  8 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.3-2
- Change some comments

* Thu Dec  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.3-1
- Initial package
