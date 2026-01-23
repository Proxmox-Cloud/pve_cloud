resource "pxc_cloud_age_secret" "route53" {
  secret_name = "aws-route53-global"
  b64_age_data = "" # output of `age -R ~/.ssh/id_ed25519.pub aws-route53-global.json | base64 -w0`
}