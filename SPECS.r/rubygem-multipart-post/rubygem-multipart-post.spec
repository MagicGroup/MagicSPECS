# Generated from multipart-post-1.1.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name multipart-post

Summary: Creates a multipart form post accessory for Net::HTTP
Name: rubygem-%{gem_name}
Version: 2.0.0
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/nicksieger/multipart-post
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Use with Net::HTTP to do multipart form posts.  IO values that
have #content_type, #original_filename, and #local_path will
be posted as a binary file.


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
pushd %{buildroot}%{gem_instdir}
# To run the tests using minitest 5
ruby -rminitest/autorun -Ilib - << \EOF
  module Kernel
    alias orig_require require
    remove_method :require

    def require path
      orig_require path unless path == 'test/unit'
    end

  end

  Test = Minitest

  Dir.glob "./test/**/test_*.rb", &method(:require)
EOF
popd

%files
%doc %{gem_instdir}/README.md
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/%{gem_name}.gemspec
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/History.txt
%{gem_instdir}/Rakefile
%{gem_instdir}/test


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.0.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 17 2014 Vít Ondruch <vondruch@redhat.com> - 2.0.0-1
- Update to multipart-post 2.0.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 1.2.0-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Upgrade to mutipart-post 1.2.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.4-1
- Rebuilt for Ruby 1.9.3.
- Upgraded to multipart-post 1.1.4.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 Vít Ondruch <vondruch@redhat.com> - 1.1.2-1
- Initial package
