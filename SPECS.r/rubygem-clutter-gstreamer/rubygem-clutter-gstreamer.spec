%global gem_name clutter-gstreamer

Name:		rubygem-%{gem_name}
Version:	2.2.5
Release:	3%{?dist}

Summary:	Ruby binding of Clutter-GStreamer
License:	LGPLv2+
URL:		http://ruby-gnome2.sourceforge.jp/
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://raw.githubusercontent.com/ruby-gnome2/ruby-gnome2/master/COPYING.LIB
# renamed to avoid namespace collision on sourcedir
Source1:	COPYING.LIB.clutter-gstreamer

BuildRequires:	rubygems-devel
# %%check
BuildRequires:	rubygem(clutter)
BuildRequires:	rubygem(gdk_pixbuf2)
BuildRequires:	rubygem(gstreamer)
BuildRequires:	rubygem-glib2-devel
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(test-unit-notify) 
BuildRequires:	%{_bindir}/xvfb-run
# See bug 904851 and below
BuildRequires:	mesa-dri-drivers
BuildRequires:	clutter-gst2
Requires:	clutter-gst2

BuildArch:		noarch

%description
Ruby/ClutterGStreamer is a Ruby binding of Clutter-GStreamer.

%package	doc
Summary:	Documentation for %{name}
Group:	Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

find . -name \*.rb -print0 | xargs --null chmod 0644

# Adjust rubygems-gnome2 requirement to be more flexible
sed -i -e 's|= 2\.2\.5|>= 2.2.5|' %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

install -cpm 644 %{SOURCE1} %{buildroot}%{gem_instdir}/COPYING.LIB

pushd %{buildroot}%{gem_instdir}
rm -rf \
	Rakefile \
	test/ \
	%{nil}
popd

%check
pushd .%{gem_instdir}

mkdir tmp
touch \
	tmp/gobject-introspection-test-utils.rb \
	tmp/clutter-test-utils.rb

# Clutter-CRITICAL **:Unable to initialize Clutter: 
# Unable to find suitable fbconfig for the GLX context: 
# Failed to find any compatible fbconfigs
#
# So use screen depth 24, see bug 904851

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
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.2.5-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.5-1
- 2.2.5

* Tue Mar 17 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.4-1
- Initial package
